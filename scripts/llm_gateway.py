import asyncio
import json
import os
import shutil
import time
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI(title="Research Pipeline LLM Gateway")

GATEWAY_API_KEY = os.getenv(
    "GATEWAY_API_KEY",
    os.getenv("RESEARCH_GATEWAY_API_KEY", "local-dev-key"),
)

MODEL_ALIAS_ENVS = {
    "research-default": "RESEARCH_DEFAULT_MODEL",
    "research_default": "RESEARCH_DEFAULT_MODEL",
    "research-strong": "RESEARCH_STRONG_MODEL",
    "research_strong": "RESEARCH_STRONG_MODEL",
    "research-fast": "RESEARCH_FAST_MODEL",
    "research_fast": "RESEARCH_FAST_MODEL",
    "research-code": "RESEARCH_CODE_MODEL",
    "research_code": "RESEARCH_CODE_MODEL",
    "research-review": "RESEARCH_REVIEW_MODEL",
    "research_review": "RESEARCH_REVIEW_MODEL",
    "research-citation": "RESEARCH_CITATION_MODEL",
    "research_citation": "RESEARCH_CITATION_MODEL",
}


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def resolve_model(requested_model: str, default_model: str) -> str:
    if requested_model in {"", "default", "auto"}:
        return default_model

    alias_env = MODEL_ALIAS_ENVS.get(requested_model)
    if alias_env:
        return os.getenv(alias_env) or default_model or requested_model

    return requested_model


def resolve_codex_model(requested_model: str, default_model: str) -> str:
    resolved = resolve_model(requested_model, default_model)
    if requested_model in MODEL_ALIAS_ENVS and resolved == requested_model:
        return ""
    return resolved


def build_providers() -> List[Dict[str, Any]]:
    providers: List[Dict[str, Any]] = []

    if env_flag("CODEX_CLI_ENABLED"):
        providers.append(
            {
                "name": "codex-cli",
                "type": "codex_cli",
                "command": os.getenv("CODEX_CLI_COMMAND", "codex"),
                "model": os.getenv("CODEX_CLI_MODEL", ""),
                "reasoning_effort": os.getenv("CODEX_CLI_REASONING_EFFORT", ""),
                "sandbox": os.getenv("CODEX_CLI_SANDBOX", "read-only"),
                "cwd": os.getenv("CODEX_CLI_CWD", os.getcwd()),
                "timeout_sec": env_int("CODEX_CLI_TIMEOUT_SEC", 900),
            }
        )

    providers.extend(
        [
            {
                "name": "hackclub",
                "type": "http",
                "base_url": os.getenv(
                    "HACKCLUB_BASE_URL",
                    "https://ai.hackclub.com/proxy/v1",
                ),
                "api_key": os.getenv("HACKCLUB_API_KEY"),
                "model": os.getenv("HACKCLUB_MODEL", "qwen/qwen3-32b"),
            },
            {
                "name": "deepseek",
                "type": "http",
                "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            },
        ]
    )
    return providers


PROVIDERS = build_providers()


def check_auth(authorization: Optional[str]) -> None:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    expected = f"Bearer {GATEWAY_API_KEY}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Invalid gateway API key")


def should_fallback(status_code: int) -> bool:
    """
    Fallback only for quota, rate limit, timeout, or server problems.
    Do not fallback on 400-level request bugs because that hides real config errors.
    """
    return status_code in {402, 408, 409, 429, 500, 502, 503, 504}


def rewrite_payload_for_provider(
    payload: Dict[str, Any],
    provider: Dict[str, Any],
) -> Dict[str, Any]:
    new_payload = dict(payload)

    requested_model = str(
        new_payload.get("model", "research-default") or "research-default"
    )
    new_payload["model"] = resolve_model(
        requested_model,
        str(provider.get("model") or ""),
    )

    # Disable streaming for now. Streaming fallback is annoying to debug.
    if new_payload.get("stream"):
        new_payload["stream"] = False

    return new_payload


async def call_provider(
    provider: Dict[str, Any],
    endpoint: str,
    payload: Dict[str, Any],
) -> httpx.Response:
    if not provider.get("api_key"):
        raise RuntimeError(f"Missing API key for provider: {provider['name']}")

    url = provider["base_url"].rstrip("/") + endpoint
    provider_payload = rewrite_payload_for_provider(payload, provider)

    headers = {
        "Authorization": f"Bearer {provider['api_key']}",
        "Content-Type": "application/json",
    }

    timeout = httpx.Timeout(
        connect=20.0,
        read=300.0,
        write=60.0,
        pool=20.0,
    )

    async with httpx.AsyncClient(timeout=timeout) as client:
        return await client.post(url, headers=headers, json=provider_payload)


def message_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
                else:
                    parts.append(json.dumps(item, ensure_ascii=False))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)

    if content is None:
        return ""

    return str(content)


def build_codex_prompt(payload: Dict[str, Any]) -> str:
    messages = payload.get("messages")
    if not isinstance(messages, list):
        raise ValueError("Codex CLI provider requires a messages list")

    instructions = [
        "You are serving one stateless OpenAI-compatible chat completion request through a local gateway.",
        "Return only the assistant message content.",
        "Do not inspect or modify local files, and do not run shell commands, unless the conversation explicitly asks you to.",
    ]

    response_format = payload.get("response_format")
    if (
        isinstance(response_format, dict)
        and response_format.get("type") == "json_object"
    ):
        instructions.append("Return valid JSON only, with no surrounding commentary.")

    sections = ["\n".join(instructions)]
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role", "user") or "user")
        content = message_content_to_text(message.get("content"))
        sections.append(f"<{role}>\n{content}\n</{role}>")

    sections.append("Answer the final user message now.")
    return "\n\n".join(sections)


def approx_tokens(text: str) -> int:
    return max(1, len(text.split())) if text else 0


def codex_chat_response(
    model: str,
    content: str,
    payload: Dict[str, Any],
    prompt_text: str,
) -> Dict[str, Any]:
    prompt_tokens = approx_tokens(prompt_text)
    completion_tokens = approx_tokens(content)

    return {
        "id": f"chatcmpl-gateway-{int(time.time() * 1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model or "codex-cli",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


async def call_codex_cli(
    provider: Dict[str, Any],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    command = str(provider.get("command") or "codex")
    if not shutil.which(command) and not os.path.exists(command):
        raise RuntimeError(f"Codex CLI command not found: {command}")

    sandbox = str(provider.get("sandbox") or "read-only")
    if sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise RuntimeError(f"Invalid CODEX_CLI_SANDBOX: {sandbox}")

    requested_model = str(
        payload.get("model", "research-default") or "research-default"
    )
    codex_model = resolve_codex_model(
        requested_model,
        str(provider.get("model") or ""),
    )
    prompt = build_codex_prompt(payload)

    cmd = [
        command,
        "-a",
        "never",
        "exec",
        "--ephemeral",
        "--sandbox",
        sandbox,
        "--cd",
        str(provider.get("cwd") or os.getcwd()),
        "--color",
        "never",
    ]
    if codex_model:
        cmd.extend(["--model", codex_model])
    reasoning_effort = str(provider.get("reasoning_effort") or "")
    if reasoning_effort:
        cmd.extend(["-c", f"model_reasoning_effort={json.dumps(reasoning_effort)}"])
    cmd.append("-")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(prompt.encode("utf-8")),
            timeout=int(provider.get("timeout_sec") or 900),
        )
    except asyncio.TimeoutError as exc:
        proc.kill()
        await proc.communicate()
        raise RuntimeError("Codex CLI timed out") from exc

    stdout_text = stdout.decode("utf-8", errors="replace").strip()
    stderr_text = stderr.decode("utf-8", errors="replace").strip()

    if proc.returncode != 0:
        detail = stderr_text or stdout_text or "no output"
        raise RuntimeError(
            f"Codex CLI failed with exit code {proc.returncode}: {detail[:1500]}"
        )

    if not stdout_text:
        raise RuntimeError(
            f"Codex CLI returned no final message: {stderr_text[:1500]}"
        )

    return codex_chat_response(codex_model, stdout_text, payload, prompt)


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "providers": [
            {
                "name": provider["name"],
                "type": provider.get("type", "http"),
                "configured": (
                    bool(
                        shutil.which(str(provider.get("command") or ""))
                        or os.path.exists(str(provider.get("command") or ""))
                    )
                    if provider.get("type") == "codex_cli"
                    else bool(provider.get("api_key"))
                ),
                "base_url": provider.get("base_url", ""),
                "model": provider.get("model") or "codex default",
            }
            for provider in PROVIDERS
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(
    request: Request,
    authorization: Optional[str] = Header(default=None),
):
    check_auth(authorization)

    payload = await request.json()
    errors: List[Dict[str, Any]] = []

    # Important: every new request starts with Hack Club again.
    for provider in PROVIDERS:
        try:
            if provider.get("type") == "codex_cli":
                data = await call_codex_cli(provider, payload)
                data["_gateway_provider"] = provider["name"]
                return JSONResponse(content=data, status_code=200)

            response = await call_provider(provider, "/chat/completions", payload)

            if response.status_code < 400:
                data = response.json()
                data["_gateway_provider"] = provider["name"]
                return JSONResponse(content=data, status_code=response.status_code)

            error_text = response.text[:1500]
            print(f"[gateway] {provider['name']} failed: {response.status_code} {error_text}")
            errors.append(
                {
                    "provider": provider["name"],
                    "status_code": response.status_code,
                    "error": error_text,
                }
            )

            if not should_fallback(response.status_code):
                raise HTTPException(
                    status_code=response.status_code,
                    detail={
                        "message": "Provider returned a non-fallback error",
                        "provider": provider["name"],
                        "error": error_text,
                    },
                )

        except (
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.ReadError,
            RuntimeError,
            ValueError,
        ) as error:
            errors.append(
                {
                    "provider": provider["name"],
                    "status_code": None,
                    "error": repr(error),
                }
            )
            continue

    raise HTTPException(
        status_code=503,
        detail={
            "message": "All providers failed",
            "errors": errors,
        },
    )
