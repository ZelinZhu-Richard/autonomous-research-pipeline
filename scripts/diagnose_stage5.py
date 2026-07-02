from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "reports" / "debug"


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def md_value(value: Any) -> str:
    if value is None or value == "":
        return ""
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    return text[:240] + "..." if len(text) > 240 else text


def compact_json(value: Any) -> str:
    if value is None:
        return "Missing or unreadable."
    return "```json\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n```"


def status_line(path: Path, run_dir: Path) -> str:
    return f"`{rel(path, run_dir)}`" if path.exists() else "Missing"


def format_candidate_table(candidates: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| # | Title | Year | Venue | Source | Citations | DOI | URL |",
        "|---:|---|---:|---|---|---:|---|---|",
    ]

    for idx, row in enumerate(candidates[:10], start=1):
        url = md_value(row.get("url"))
        doi = md_value(row.get("doi"))
        title = md_value(row.get("title"))
        venue = md_value(row.get("venue"))
        source = md_value(row.get("source"))
        year = md_value(row.get("year"))
        citations = md_value(row.get("citation_count"))
        lines.append(
            f"| {idx} | {title} | {year} | {venue} | {source} | {citations} | {doi} | {url} |"
        )

    return lines


def write_report(run_dir: Path, run_id: str) -> Path:
    stage04 = run_dir / "stage-04"
    stage05 = run_dir / "stage-05"
    stage06 = run_dir / "stage-06"

    candidates_path = stage04 / "candidates.jsonl"
    refs_path = stage04 / "references.bib"
    search_meta_path = stage04 / "search_meta.json"
    screen_meta_path = stage05 / "screen_meta.json"
    stage05_health_path = stage05 / "stage_health.json"
    stage05_decision_path = stage05 / "decision.json"
    stage06_decision_path = stage06 / "decision.json"

    candidates = load_jsonl(candidates_path)
    shortlist_paths = sorted(run_dir.rglob("shortlist.jsonl"))
    shortlist_path = shortlist_paths[0] if shortlist_paths else None
    shortlist_rows = load_jsonl(shortlist_path) if shortlist_path else []

    search_meta = load_json(search_meta_path)
    screen_meta = load_json(screen_meta_path)
    stage05_health = load_json(stage05_health_path)
    stage05_decision = load_json(stage05_decision_path)
    stage06_decision = load_json(stage06_decision_path)

    stage05_error = ""
    if stage05_health:
        stage05_error = str(stage05_health.get("error") or "")
    if not stage05_error and stage05_decision:
        stage05_error = str(stage05_decision.get("error") or "")

    stage06_error = str(stage06_decision.get("error") or "") if stage06_decision else ""
    empty_shortlist = not shortlist_path or len(shortlist_rows) == 0
    stage05_blocker = bool(stage05_error) or (
        screen_meta is not None and screen_meta.get("shortlist_size") == 0
    )

    lines = [
        f"# Stage 5 Diagnostic: {run_id}",
        "",
        "## Run",
        "",
        f"- Run directory: `{run_dir}`",
        f"- Candidates: {len(candidates)} rows in {status_line(candidates_path, run_dir)}",
        f"- References: {status_line(refs_path, run_dir)}",
        f"- Shortlist: {status_line(shortlist_path, run_dir) if shortlist_path else 'Missing'}",
        f"- Shortlist rows: {len(shortlist_rows)}",
        "",
        "## Stage 5 Status",
        "",
        f"- Health file: {status_line(stage05_health_path, run_dir)}",
        f"- Decision file: {status_line(stage05_decision_path, run_dir)}",
        f"- Status: {md_value(stage05_health.get('status') if stage05_health else None)}",
        f"- Decision: {md_value(stage05_decision.get('decision') if stage05_decision else None)}",
        f"- Error: {md_value(stage05_error) or 'None reported.'}",
        f"- Duration seconds: {md_value(stage05_health.get('duration_sec') if stage05_health else None)}",
        f"- Timestamp: {md_value(stage05_health.get('timestamp') if stage05_health else None)}",
        "",
        "## Stage 5 Metadata",
        "",
        compact_json(screen_meta),
        "",
        "## Stage 6 Status",
        "",
        f"- Decision file: {status_line(stage06_decision_path, run_dir)}",
        f"- Status: {md_value(stage06_decision.get('status') if stage06_decision else None)}",
        f"- Decision: {md_value(stage06_decision.get('decision') if stage06_decision else None)}",
        f"- Error: {md_value(stage06_error) or 'None reported.'}",
        "",
        "## Search Metadata",
        "",
        compact_json(search_meta),
        "",
        "## Sample Candidates",
        "",
    ]
    lines.extend(format_candidate_table(candidates))

    lines.extend(
        [
            "",
            "## Diagnosis",
            "",
            f"- Stage 5 empty-shortlist blocker detected: {stage05_blocker}",
            f"- Stage 6 missing-shortlist failure detected: {'shortlist.jsonl' in stage06_error or (empty_shortlist and stage06_decision is not None)}",
            "- Stage 6 appears downstream of Stage 5: knowledge extraction requires `shortlist.jsonl`, but Stage 5 produced no shortlist.",
            "- No raw run artifacts were modified by this diagnostic.",
            "",
            "## Recommended Next Actions",
            "",
            "1. Inspect the sample candidates and Stage 4 search metadata for topic drift before rerunning.",
            "2. Tune or rerun Stage 5 screening with less brittle criteria or improved retrieval queries.",
            "3. Keep `shortlist.jsonl` recovery as an explicit operator-approved action; do not fabricate it during diagnostics.",
            "4. Re-extract the run and rebuild the leaderboard after a repaired rerun produces a real shortlist.",
            "",
        ]
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{run_id}_stage5.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/diagnose_stage5.py <run_dir> <run_id>")
        return 1

    run_dir = Path(sys.argv[1]).expanduser().resolve()
    run_id = sys.argv[2]

    if not run_dir.exists():
        print(f"Run directory not found: {run_dir}")
        return 1
    if not run_dir.is_dir():
        print(f"Run path is not a directory: {run_dir}")
        return 1

    out_path = write_report(run_dir, run_id)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
