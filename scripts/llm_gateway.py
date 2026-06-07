import os
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI(title="Research Pipeline LLM Gateway")

GATEWAY_API_KEY = os.getenv("GATEWAY_API_KEY", "local-dev-key")

PROVIDERS = [
    {
        "name": "hackclub",
        "base_url": os.getenv("HACKCLUB_BASE_URL", "https://ai.hackclub.com/proxy/v1"),
        "api_key": os.getenv("HACKCLUB_API_KEY"),
        "model": os.getenv("HACKCLUB_MODEL", "qwen/qwen3-32b"),
    },
    {
        "name": "deepseek",
        "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    },
]


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

    requested_model = new_payload.get("model", "research-default")

    if requested_model in {"research-default", "default", "auto"}:
        new_payload["model"] = provider["model"]

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


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "providers": [
            {
                "name": provider["name"],
                "configured": bool(provider.get("api_key")),
                "base_url": provider["base_url"],
                "model": provider["model"],
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

        except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError, RuntimeError) as error:
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