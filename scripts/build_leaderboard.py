from __future__ import annotations

import json
from pathlib import Path


REGISTRY = Path("registries/idea_registry.jsonl")
OUT = Path("reports/leaderboard.md")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def score_run(row: dict) -> int:
    score = 0

    if row.get("goal_exists"):
        score += 10
    if row.get("problem_tree_exists"):
        score += 10
    if row.get("candidate_count", 0) > 0:
        score += 15
    if row.get("shortlist_count", 0) > 0:
        score += 20
    if row.get("references_exists"):
        score += 10
    if row.get("experiment_plan_exists"):
        score += 20
    if row.get("paper_tex_exists"):
        score += 10
    if row.get("paper_pdf_exists"):
        score += 5

    if row.get("failure_markers"):
        score -= 15

    return max(score, 0)


def dedupe_latest_by_run_id(rows: list[dict]) -> list[dict]:
    latest_by_run_id: dict[str, dict] = {}
    no_id_rows: list[dict] = []

    for row in rows:
        run_id = str(row.get("run_id") or "")
        if not run_id:
            no_id_rows.append(row)
            continue

        existing = latest_by_run_id.get(run_id)
        if existing is None or str(row.get("created_at") or "") >= str(existing.get("created_at") or ""):
            latest_by_run_id[run_id] = row

    return no_id_rows + list(latest_by_run_id.values())


def main() -> int:
    rows = dedupe_latest_by_run_id(load_jsonl(REGISTRY))

    if not rows:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text("# Research Run Leaderboard\n\nNo runs extracted yet.\n")
        print("No registry rows found.")
        return 0

    scored = []
    for row in rows:
        scored.append((score_run(row), row))

    scored.sort(key=lambda x: x[0], reverse=True)

    lines = [
        "# Research Run Leaderboard",
        "",
        "| Rank | Run ID | Score | Status | Candidates | Shortlist | Paper | Failures |",
        "|---:|---|---:|---|---:|---:|---|---:|",
    ]

    for i, (score, row) in enumerate(scored, start=1):
        paper = "PDF" if row.get("paper_pdf_exists") else "TeX" if row.get("paper_tex_exists") else "No"
        failures = len(row.get("failure_markers", []))
        lines.append(
            f"| {i} | `{row.get('run_id', '')}` | {score} | "
            f"{row.get('status', '')} | {row.get('candidate_count', 0)} | "
            f"{row.get('shortlist_count', 0)} | {paper} | {failures} |"
        )

    lines += [
        "",
        "## Scoring",
        "",
        "- goal.md: 10",
        "- problem_tree.md: 10",
        "- candidates found: 15",
        "- shortlist found: 20",
        "- references.bib: 10",
        "- experiment plan: 20",
        "- TeX paper: 10",
        "- PDF paper: 5",
        "- failure markers: -15",
        "",
        "This is an infrastructure score, not a research-quality score.",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
