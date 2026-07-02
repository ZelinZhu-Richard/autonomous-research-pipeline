from __future__ import annotations

import logging
import os
import threading
import time
from collections.abc import Callable
from typing import Any


logger = logging.getLogger(__name__)


class LiteratureSourceUnavailable(RuntimeError):
    """Raised when a literature source is rate-limited or temporarily down."""


class OpenAlexUnavailable(LiteratureSourceUnavailable):
    """Raised when OpenAlex is unavailable after retries or breaker cooldown."""


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        logger.warning("Invalid %s=%r; using %.1f", name, raw, default)
        return default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        logger.warning("Invalid %s=%r; using %d", name, raw, default)
        return default


def _patch_nullable_request(
    module: Any,
    *,
    flag_name: str,
    source_name: str,
) -> None:
    if getattr(module, flag_name, False):
        return

    original_request = module._request_with_retry

    def hardened_request(*args: Any, **kwargs: Any) -> dict[str, Any]:
        data = original_request(*args, **kwargs)
        if data is None:
            raise LiteratureSourceUnavailable(
                f"{source_name} unavailable or circuit breaker open"
            )
        return data

    setattr(module, f"{flag_name}_original_request", original_request)
    module._request_with_retry = hardened_request
    setattr(module, flag_name, True)


def _patch_openalex(openalex_mod: Any) -> None:
    flag_name = "_arp_openalex_hardened"
    if getattr(openalex_mod, flag_name, False):
        return

    original_request = openalex_mod._request_with_retry
    threshold = max(1, _env_int("ARC_OPENALEX_CB_THRESHOLD", 3))
    initial_cooldown = max(1.0, _env_float("ARC_OPENALEX_CB_COOLDOWN_SEC", 300.0))
    max_cooldown = max(
        initial_cooldown,
        _env_float("ARC_OPENALEX_CB_MAX_COOLDOWN_SEC", 1800.0),
    )
    lock = threading.Lock()
    state = {
        "failures": 0,
        "trips": 0,
        "open_until": 0.0,
    }

    def record_success() -> None:
        with lock:
            state["failures"] = 0
            state["trips"] = 0
            state["open_until"] = 0.0

    def record_failure(reason: str) -> None:
        with lock:
            state["failures"] += 1
            if state["failures"] < threshold:
                return
            cooldown = min(initial_cooldown * (2 ** state["trips"]), max_cooldown)
            state["trips"] += 1
            state["failures"] = 0
            state["open_until"] = time.monotonic() + cooldown
        logger.warning(
            "OpenAlex circuit breaker OPEN for %.0fs after %s. "
            "ARC will try cache and remaining literature sources.",
            cooldown,
            reason,
        )

    def hardened_request(url: str, email: str) -> dict[str, Any]:
        with lock:
            remaining = state["open_until"] - time.monotonic()
        if remaining > 0:
            logger.warning(
                "OpenAlex circuit breaker OPEN; skipping request for %.0fs",
                remaining,
            )
            raise OpenAlexUnavailable("OpenAlex circuit breaker open")

        try:
            data = original_request(url, email)
        except Exception:
            record_failure("request exception")
            raise

        if data is None:
            record_failure("exhausted retries")
            raise OpenAlexUnavailable("OpenAlex request exhausted retries")

        record_success()
        return data

    openalex_mod._arp_openalex_original_request = original_request
    openalex_mod._request_with_retry = hardened_request
    openalex_mod._arp_openalex_state = state
    setattr(openalex_mod, flag_name, True)


def _patch_arxiv(arxiv_mod: Any, search_mod: Any | None) -> None:
    flag_name = "_arp_arxiv_hardened"
    if getattr(arxiv_mod, flag_name, False):
        return

    original_should_allow: Callable[[], bool] = arxiv_mod._cb_should_allow
    original_on_failure: Callable[[], bool] = arxiv_mod._cb_on_failure
    original_search: Callable[..., list[Any]] = arxiv_mod.search_arxiv

    def hardened_should_allow() -> bool:
        allowed = original_should_allow()
        if not allowed:
            raise LiteratureSourceUnavailable("arXiv circuit breaker open")
        return True

    def hardened_on_failure() -> bool:
        original_on_failure()
        raise LiteratureSourceUnavailable("arXiv unavailable or rate limited")

    def hardened_search(*args: Any, **kwargs: Any) -> list[Any]:
        if getattr(arxiv_mod, "arxiv", None) is None:
            raise LiteratureSourceUnavailable("arXiv library is not installed")
        return original_search(*args, **kwargs)

    arxiv_mod._arp_arxiv_original_should_allow = original_should_allow
    arxiv_mod._arp_arxiv_original_on_failure = original_on_failure
    arxiv_mod._arp_arxiv_original_search = original_search
    arxiv_mod._cb_should_allow = hardened_should_allow
    arxiv_mod._cb_on_failure = hardened_on_failure
    arxiv_mod.search_arxiv = hardened_search
    if search_mod is not None:
        search_mod.search_arxiv = hardened_search
    setattr(arxiv_mod, flag_name, True)


def apply() -> None:
    """Apply repo-local literature source hardening for ARC runs."""
    if os.environ.get("ARC_LITERATURE_HARDENING", "1").strip().lower() in {
        "0",
        "false",
        "no",
        "off",
    }:
        logger.info("ARC literature hardening disabled by ARC_LITERATURE_HARDENING")
        return

    from researchclaw.literature import arxiv_client
    from researchclaw.literature import openalex_client
    from researchclaw.literature import semantic_scholar
    from researchclaw.literature import search as search_mod

    _patch_openalex(openalex_client)
    _patch_nullable_request(
        semantic_scholar,
        flag_name="_arp_s2_hardened",
        source_name="Semantic Scholar",
    )
    _patch_arxiv(arxiv_client, search_mod)
    logger.debug("ARC literature hardening applied")
