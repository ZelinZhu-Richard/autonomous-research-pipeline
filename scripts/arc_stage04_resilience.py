from __future__ import annotations

import json
import logging
import os
import random
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


logger = logging.getLogger(__name__)

_MIN_USABLE_SOURCES = 5
_MAX_TOTAL_FAILURES = 8
_PROVIDER_LIMIT = 20


@dataclass
class ProviderState:
    name: str
    threshold: int
    failures: int = 0
    attempts: int = 0
    successes: int = 0
    disabled: bool = False
    disabled_reason: str = ""
    cooldown_until: float = 0.0
    last_error: str = ""

    def status(self, now: float) -> str:
        if self.disabled:
            return "disabled"
        if self.cooldown_until > now:
            return "cooling"
        return "active"

    def to_dict(self) -> dict[str, Any]:
        now = time.monotonic()
        return {
            "name": self.name,
            "status": self.status(now),
            "failures": self.failures,
            "attempts": self.attempts,
            "successes": self.successes,
            "threshold": self.threshold,
            "disabled_reason": self.disabled_reason,
            "cooldown_remaining_sec": max(0.0, round(self.cooldown_until - now, 1)),
            "last_error": self.last_error,
        }


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _env_float(name: str, default: float) -> float:
    raw = str(os.environ.get(name, "")).strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _request_delay() -> tuple[float, float]:
    low = max(0.0, _env_float("ARC_STAGE04_REQUEST_DELAY_MIN_SEC", 5.0))
    high = max(low, _env_float("ARC_STAGE04_REQUEST_DELAY_MAX_SEC", 10.0))
    return low, high


def _sleep(seconds: float) -> None:
    if seconds <= 0:
        return
    time.sleep(seconds)


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
        + ("\n" if rows else ""),
        encoding="utf-8",
    )


def _normalise_title(title: str) -> str:
    text = title.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_candidate(paper: Any, provider: str, query: str) -> dict[str, Any]:
    if hasattr(paper, "to_dict"):
        row = dict(paper.to_dict())
    elif isinstance(paper, dict):
        row = dict(paper)
    else:
        row = {"title": str(paper)}

    row.setdefault("source", provider)
    row.setdefault(
        "paper_id",
        row.get("id") or f"{provider}-{abs(hash(row.get('title', '')))}",
    )
    row.setdefault("authors", [])
    row.setdefault("year", 0)
    row.setdefault("abstract", "")
    row.setdefault("venue", "")
    row.setdefault("citation_count", 0)
    row.setdefault("doi", "")
    row.setdefault("arxiv_id", "")
    row.setdefault("url", "")
    row["source"] = row.get("source") or provider
    row["provider_query"] = query
    row["collected_at"] = _utcnow_iso()
    return row


def _dedupe_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    for row in rows:
        title = str(row.get("title") or "").strip()
        if not title:
            continue
        doi = str(row.get("doi") or "").strip().lower()
        arxiv_id = str(row.get("arxiv_id") or "").strip().lower()
        key = doi or (f"arxiv:{arxiv_id}" if arxiv_id else _normalise_title(title))
        if not key:
            continue
        if key not in best:
            best[key] = row
            order.append(key)
            continue
        old = best[key]
        if _safe_int(row.get("citation_count")) > _safe_int(old.get("citation_count")):
            best[key] = row

    return [best[key] for key in order]


def _is_usable(row: dict[str, Any]) -> bool:
    if row.get("is_placeholder"):
        return False
    title = str(row.get("title") or "").strip()
    if not title:
        return False
    if str(row.get("source") or "") == "manual_seed":
        return True
    return bool(row.get("url") or row.get("doi") or row.get("arxiv_id"))


def _manual_seed_paths(run_dir: Path, stage_dir: Path) -> list[Path]:
    return [run_dir / "literature_seed.md", stage_dir / "literature_seed.md"]


def _parse_manual_seed_line(line: str, index: int) -> dict[str, Any] | None:
    raw = line.strip()
    raw = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", raw).strip()
    if not raw or raw.startswith("#"):
        return None

    link_match = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", raw)
    url_match = re.search(r"https?://\S+", raw)
    doi_match = re.search(r"\b10\.\d{4,9}/[^\s),;]+", raw)
    year_match = re.search(r"\b(19|20)\d{2}\b", raw)

    if link_match:
        title = link_match.group(1).strip()
        url = link_match.group(2).strip()
    else:
        url = url_match.group(0).rstrip(").,;") if url_match else ""
        title = raw
        if url:
            title = title.replace(url, "")
        if doi_match:
            title = title.replace(doi_match.group(0), "")
        title = re.sub(r"\bdoi\s*:\s*", "", title, flags=re.I)
        title = title.strip(" -:;,.")

    if not title:
        return None

    return {
        "paper_id": f"manual-seed-{index}",
        "title": title,
        "authors": [],
        "year": _safe_int(year_match.group(0) if year_match else 0),
        "abstract": "Manual literature seed supplied by the operator.",
        "venue": "",
        "citation_count": 0,
        "doi": doi_match.group(0) if doi_match else "",
        "arxiv_id": "",
        "url": url,
        "source": "manual_seed",
        "collected_at": _utcnow_iso(),
    }


def _load_manual_seed(
    run_dir: Path,
    stage_dir: Path,
) -> tuple[list[dict[str, Any]], str]:
    for path in _manual_seed_paths(run_dir, stage_dir):
        if not path.exists():
            continue
        rows: list[dict[str, Any]] = []
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for index, line in enumerate(lines, start=1):
            row = _parse_manual_seed_line(line, index)
            if row is not None:
                rows.append(row)
        return rows, str(path)
    return [], ""


def _candidate_bibtex(row: dict[str, Any]) -> str:
    key_source = re.sub(
        r"[^a-zA-Z0-9]",
        "",
        str(row.get("title", "paper")).lower(),
    )[:24]
    key = str(
        row.get("cite_key")
        or f"manual{row.get('year') or '0000'}{key_source}"
        or "manual0000"
    )
    title = str(row.get("title") or "Untitled")
    year = str(row.get("year") or "Unknown")
    url = str(row.get("url") or "")
    doi = str(row.get("doi") or "")
    authors = row.get("authors") or []
    author_names: list[str] = []
    if isinstance(authors, list):
        for author in authors:
            if isinstance(author, dict):
                name = str(author.get("name") or "").strip()
            else:
                name = str(author).strip()
            if name:
                author_names.append(name)
    lines = [
        f"@article{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{' and '.join(author_names) or 'Unknown'}}},",
        f"  year = {{{year}}},",
    ]
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    if url:
        lines.append(f"  url = {{{url}}},")
    lines.append("}")
    return "\n".join(lines)


def _provider_status_line(providers: list[ProviderState]) -> str:
    now = time.monotonic()
    active = [p.name for p in providers if p.status(now) == "active"]
    cooling = [p.name for p in providers if p.status(now) == "cooling"]
    disabled = [p.name for p in providers if p.status(now) == "disabled"]
    return (
        f"active={active or ['none']} "
        f"cooling={cooling or ['none']} "
        f"disabled={disabled or ['none']}"
    )


def _all_unavailable(providers: list[ProviderState]) -> bool:
    now = time.monotonic()
    return all(p.status(now) != "active" for p in providers)


def _pace_request(last_request_at: float | None) -> float:
    low, high = _request_delay()
    if last_request_at is None:
        return time.monotonic()
    elapsed = time.monotonic() - last_request_at
    wait = random.uniform(low, high)
    if elapsed < wait:
        _sleep(wait - elapsed)
    return time.monotonic()


def _backoff_seconds(failures: int) -> float:
    base = min(2 ** max(0, failures - 1), 60)
    return min(60.0, base + random.uniform(0.0, max(1.0, base * 0.25)))


def _call_provider(
    provider: ProviderState,
    query: str,
    year_min: int,
    s2_api_key: str,
) -> list[Any]:
    if provider.name == "openalex":
        from researchclaw.literature.openalex_client import search_openalex

        return search_openalex(query, limit=_PROVIDER_LIMIT, year_min=year_min)
    if provider.name == "semantic_scholar":
        from researchclaw.literature.semantic_scholar import search_semantic_scholar

        return search_semantic_scholar(
            query,
            limit=_PROVIDER_LIMIT,
            year_min=year_min,
            api_key=s2_api_key,
        )
    if provider.name == "arxiv":
        from researchclaw.literature.arxiv_client import search_arxiv

        return search_arxiv(query, limit=_PROVIDER_LIMIT, year_min=year_min)
    raise RuntimeError(f"Unknown provider: {provider.name}")


def _read_queries(run_dir: Path, topic: str) -> tuple[list[str], int]:
    data = _read_json(run_dir / "stage-03" / "queries.json", {})
    queries = data.get("queries") if isinstance(data, dict) else None
    if not isinstance(queries, list) or not queries:
        queries = [topic]
    clean_queries = [str(item).strip() for item in queries if str(item).strip()]
    year_min = _safe_int(
        data.get("year_min", 2020) if isinstance(data, dict) else 2020,
        2020,
    )

    try:
        from researchclaw.pipeline.stage_impls._literature import _expand_search_queries

        expanded = _expand_search_queries(clean_queries, topic)
    except Exception:
        expanded = clean_queries
    return expanded[:10] or [topic], year_min


def _write_review(
    path: Path,
    *,
    logical_status: str,
    candidates: list[dict[str, Any]],
    usable_count: int,
    providers: list[ProviderState],
    manual_seed_path: str,
) -> None:
    lines = [
        "# Literature Collection Summary",
        "",
        f"- Status: {logical_status}",
        f"- Total candidates: {len(candidates)}",
        f"- Usable sources: {usable_count}",
        f"- Manual seed: {manual_seed_path or 'not provided'}",
        "",
        "## Provider Status",
        "",
    ]
    for provider in providers:
        info = provider.to_dict()
        lines.append(
            f"- {provider.name}: {info['status']} "
            f"(attempts={info['attempts']}, failures={info['failures']}, "
            f"successes={info['successes']})"
        )
    lines.extend(["", "## Candidate Titles", ""])
    for idx, row in enumerate(candidates[:30], start=1):
        title = str(row.get("title") or "Untitled")
        source = str(row.get("source") or "unknown")
        year = row.get("year") or ""
        url = row.get("url") or row.get("doi") or row.get("arxiv_id") or ""
        lines.append(f"{idx}. {title} ({source}, {year}) {url}".rstrip())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_stage_outputs(
    stage_dir: Path,
    *,
    candidates: list[dict[str, Any]],
    providers: list[ProviderState],
    queries: list[str],
    year_min: int,
    logical_status: str,
    manual_seed_path: str,
    failure_events: list[dict[str, Any]],
    total_failures: int,
) -> tuple[str, ...]:
    usable_count = sum(1 for row in candidates if _is_usable(row))
    candidates_path = stage_dir / "candidates.jsonl"
    raw_path = stage_dir / "literature_raw.json"
    review_path = stage_dir / "literature_review.md"
    meta_path = stage_dir / "search_meta.json"
    bib_path = stage_dir / "references.bib"

    _write_jsonl(candidates_path, candidates)
    _write_json(
        raw_path,
        {
            "logical_status": logical_status,
            "queries": queries,
            "year_min": year_min,
            "providers": [p.to_dict() for p in providers],
            "failure_events": failure_events,
            "candidates": candidates,
            "manual_seed_path": manual_seed_path,
            "ts": _utcnow_iso(),
        },
    )
    _write_review(
        review_path,
        logical_status=logical_status,
        candidates=candidates,
        usable_count=usable_count,
        providers=providers,
        manual_seed_path=manual_seed_path,
    )
    _write_json(
        meta_path,
        {
            "logical_status": logical_status,
            "real_search": any(p.successes > 0 for p in providers),
            "queries_used": queries,
            "year_min": year_min,
            "total_candidates": len(candidates),
            "usable_sources": usable_count,
            "provider_limit": _PROVIDER_LIMIT,
            "provider_status": [p.to_dict() for p in providers],
            "total_provider_failures": total_failures,
            "max_total_failures": _MAX_TOTAL_FAILURES,
            "manual_seed_path": manual_seed_path,
            "bibtex_entries": usable_count,
            "ts": _utcnow_iso(),
        },
    )

    artifacts = ["candidates.jsonl", "literature_raw.json", "literature_review.md"]
    usable_rows = [row for row in candidates if _is_usable(row)]
    if usable_rows:
        bib_path.write_text(
            "\n\n".join(_candidate_bibtex(row) for row in usable_rows) + "\n",
            encoding="utf-8",
        )
        artifacts.append("references.bib")
    artifacts.append("search_meta.json")
    return tuple(artifacts)


def hardened_literature_collect(
    stage_dir: Path,
    run_dir: Path,
    config: Any,
    adapters: Any,
    *,
    llm: Any | None = None,
    prompts: Any | None = None,
) -> Any:
    from researchclaw.pipeline._helpers import StageResult
    from researchclaw.pipeline.stages import Stage, StageStatus

    _ = adapters, llm, prompts
    topic = str(getattr(getattr(config, "research", object()), "topic", "") or "")
    queries, year_min = _read_queries(run_dir, topic)
    s2_api_key = str(getattr(getattr(config, "llm", object()), "s2_api_key", "") or "")

    providers = [
        ProviderState("openalex", threshold=3),
        ProviderState("semantic_scholar", threshold=3),
        ProviderState("arxiv", threshold=2),
    ]
    candidates: list[dict[str, Any]] = []
    failure_events: list[dict[str, Any]] = []
    total_failures = 0
    last_request_at: float | None = None

    manual_rows, manual_seed_path = _load_manual_seed(run_dir, stage_dir)
    if manual_rows:
        candidates = _dedupe_candidates(candidates + manual_rows)
        print(
            f"[stage04] Loaded {len(manual_rows)} manual literature seed entries "
            f"from {manual_seed_path}"
        )

    print(
        f"[stage04] Hardened literature collection: {len(queries)} queries, "
        f"providers=openalex, semantic_scholar, arxiv, limit={_PROVIDER_LIMIT}"
    )

    for query_index, query in enumerate(queries, start=1):
        print(
            f"[stage04] Query {query_index}/{len(queries)}: {query!r} | "
            f"{_provider_status_line(providers)}"
        )
        if total_failures >= _MAX_TOTAL_FAILURES or _all_unavailable(providers):
            print(
                "[stage04] Stopping provider loop: all providers are disabled/cooling "
                "or failure cap reached."
            )
            break

        for provider in providers:
            now = time.monotonic()
            status = provider.status(now)
            if status == "disabled":
                continue
            if status == "cooling":
                print(
                    f"[stage04] {provider.name} cooling down for "
                    f"{provider.cooldown_until - now:.1f}s; skipping this query."
                )
                continue
            if total_failures >= _MAX_TOTAL_FAILURES:
                break

            provider.attempts += 1
            last_request_at = _pace_request(last_request_at)
            try:
                papers = _call_provider(provider, query, year_min, s2_api_key)
            except Exception as exc:  # noqa: BLE001
                provider.failures += 1
                total_failures += 1
                provider.last_error = str(exc)
                failure_events.append(
                    {
                        "provider": provider.name,
                        "query": query,
                        "failure": provider.failures,
                        "threshold": provider.threshold,
                        "error": str(exc),
                        "ts": _utcnow_iso(),
                    }
                )
                if provider.failures >= provider.threshold:
                    provider.disabled = True
                    provider.disabled_reason = str(exc)
                    provider.cooldown_until = 0.0
                    print(
                        f"[stage04] Disabled {provider.name}: "
                        f"{provider.failures}/{provider.threshold} failures. "
                        f"Reason: {exc}"
                    )
                else:
                    cooldown = _backoff_seconds(provider.failures)
                    provider.cooldown_until = time.monotonic() + cooldown
                    print(
                        f"[stage04] {provider.name} failed "
                        f"{provider.failures}/{provider.threshold}; "
                        f"cooling down for {cooldown:.1f}s. Reason: {exc}"
                    )
                continue

            provider.successes += 1
            provider.failures = 0
            provider.last_error = ""
            provider.cooldown_until = 0.0
            if papers:
                rows = [_as_candidate(paper, provider.name, query) for paper in papers]
                candidates = _dedupe_candidates(candidates + rows)
            print(
                f"[stage04] {provider.name} returned {len(papers)} papers; "
                f"deduped usable total={sum(1 for row in candidates if _is_usable(row))}"
            )

        print(
            f"[stage04] After query {query_index}: "
            f"total candidates={len(candidates)}, "
            f"usable={sum(1 for row in candidates if _is_usable(row))}"
        )

    candidates = _dedupe_candidates(candidates)
    usable_count = sum(1 for row in candidates if _is_usable(row))
    had_provider_failures = bool(failure_events) or any(p.disabled for p in providers)

    if usable_count >= _MIN_USABLE_SOURCES:
        logical_status = "PARTIAL" if had_provider_failures else "DONE"
        transport_status = StageStatus.DONE
        decision = "partial" if logical_status == "PARTIAL" else "proceed"
        error = None
    else:
        logical_status = "FAILED_NEEDS_MANUAL_SEED"
        transport_status = StageStatus.FAILED
        decision = "failed_needs_manual_seed"
        error = (
            f"Stage 04 collected {usable_count} usable sources. Add literature_seed.md "
            "to the run directory or stage-04 directory, then resume from LITERATURE_COLLECT."
        )

    artifacts = _write_stage_outputs(
        stage_dir,
        candidates=candidates,
        providers=providers,
        queries=queries,
        year_min=year_min,
        logical_status=logical_status,
        manual_seed_path=manual_seed_path,
        failure_events=failure_events,
        total_failures=total_failures,
    )

    print(
        f"[stage04] Final outcome: {logical_status}; usable_sources={usable_count}; "
        f"artifacts={', '.join(artifacts)}"
    )
    if logical_status == "FAILED_NEEDS_MANUAL_SEED":
        print(
            "[stage04] Add manual seeds to literature_seed.md, for example: "
            "- Paper title (2024) https://doi.org/..."
        )

    return StageResult(
        stage=Stage.LITERATURE_COLLECT,
        status=transport_status,
        artifacts=artifacts,
        error=error,
        decision=decision,
        evidence_refs=tuple(f"stage-04/{artifact}" for artifact in artifacts),
    )


def _rewrite_logical_metadata(stage_dir: Path, result: Any) -> None:
    meta = _read_json(stage_dir / "search_meta.json", {})
    logical_status = meta.get("logical_status") if isinstance(meta, dict) else None
    if logical_status not in {"PARTIAL", "FAILED_NEEDS_MANUAL_SEED"}:
        return

    for filename in ("decision.json", "stage_health.json"):
        path = stage_dir / filename
        payload = _read_json(path, {})
        if not isinstance(payload, dict):
            continue
        payload.setdefault("transport_status", result.status.value)
        payload["status"] = logical_status
        payload["logical_status"] = logical_status
        if result.decision:
            payload["decision"] = result.decision
        if result.error:
            payload["error"] = result.error
        _write_json(path, payload)


def apply() -> None:
    from researchclaw.pipeline import executor
    from researchclaw.pipeline.stages import Stage

    if getattr(executor, "_arp_stage04_resilience_applied", False):
        return

    executor._STAGE_EXECUTORS[Stage.LITERATURE_COLLECT] = hardened_literature_collect
    executor._execute_literature_collect = hardened_literature_collect

    original_execute_stage: Callable[..., Any] = executor.execute_stage

    def wrapped_execute_stage(stage: Any, *args: Any, **kwargs: Any) -> Any:
        result = original_execute_stage(stage, *args, **kwargs)
        if stage == Stage.LITERATURE_COLLECT:
            run_dir = kwargs.get("run_dir")
            if isinstance(run_dir, Path):
                _rewrite_logical_metadata(run_dir / "stage-04", result)
        return result

    executor._arp_stage04_original_execute_stage = original_execute_stage
    executor.execute_stage = wrapped_execute_stage

    runner_mod = sys.modules.get("researchclaw.pipeline.runner")
    if runner_mod is not None:
        runner_mod.execute_stage = wrapped_execute_stage

    executor._arp_stage04_resilience_applied = True
    logger.debug("ARC Stage 04 resilience patch applied")
