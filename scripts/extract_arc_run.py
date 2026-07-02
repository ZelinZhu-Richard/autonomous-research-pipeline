from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_text(path: Path | None, limit: int = 5000) -> str:
    if not path or not path.exists():
        return ""
    return path.read_text(errors="ignore")[:limit]


def find_first(run_dir: Path, name: str) -> Path | None:
    matches = list(run_dir.rglob(name))
    return matches[0] if matches else None


def count_jsonl(path: Path | None) -> int:
    if not path or not path.exists():
        return 0
    return sum(1 for line in path.read_text(errors="ignore").splitlines() if line.strip())


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    rows = []
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


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def upsert_jsonl_by_run_id(path: Path, obj: dict) -> None:
    run_id = obj.get("run_id")
    rows = []
    replaced = False

    for row in load_jsonl(path):
        if row.get("run_id") != run_id:
            rows.append(row)
            continue
        if not replaced:
            rows.append(obj)
            replaced = True

    if not replaced:
        rows.append(obj)

    write_jsonl(path, rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/extract_arc_run.py <run_dir> <run_id>")
        return 1

    run_dir = Path(sys.argv[1]).expanduser().resolve()
    run_id = sys.argv[2]

    if not run_dir.exists():
        print(f"Run directory not found: {run_dir}")
        return 1

    project_root = Path.cwd()

    goal = find_first(run_dir, "goal.md")
    problem_tree = find_first(run_dir, "problem_tree.md")
    candidates = find_first(run_dir, "candidates.jsonl")
    shortlist = find_first(run_dir, "shortlist.jsonl")
    refs = find_first(run_dir, "references.bib")
    experiment_plan = find_first(run_dir, "experiment_plan.md")
    paper_tex = find_first(run_dir, "paper.tex") or find_first(run_dir, "main.tex")
    paper_pdf = find_first(run_dir, "paper.pdf")

    files = [p for p in run_dir.rglob("*") if p.is_file()]
    failed_markers = []

    for p in files:
        txt = read_text(p, limit=2000)
        if "FAILED" in txt or "Missing input" in txt or "blocked" in txt.lower():
            failed_markers.append(str(p.relative_to(run_dir)))

    idea_entry = {
        "run_id": run_id,
        "source": "AutoResearchClaw+MetaClaw",
        "run_dir": str(run_dir),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "goal_exists": bool(goal),
        "problem_tree_exists": bool(problem_tree),
        "candidate_count": count_jsonl(candidates),
        "shortlist_count": count_jsonl(shortlist),
        "references_exists": bool(refs),
        "experiment_plan_exists": bool(experiment_plan),
        "paper_tex_exists": bool(paper_tex),
        "paper_pdf_exists": bool(paper_pdf),
        "status": "paper_generated" if paper_pdf or paper_tex else "partial",
        "failure_markers": failed_markers[:20],
        "goal_preview": read_text(goal, limit=1000),
    }

    upsert_jsonl_by_run_id(project_root / "registries" / "idea_registry.jsonl", idea_entry)

    report_dir = project_root / "reports" / "run_cards"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{run_id}.md"

    failure_text = "\n".join("- " + x for x in failed_markers[:20]) if failed_markers else "None detected."

    report_path.write_text(
        f"""# Run Card: {run_id}

## Source
AutoResearchClaw + MetaClaw

## Run directory
`{run_dir}`

## Artifacts

- goal.md: {bool(goal)}
- problem_tree.md: {bool(problem_tree)}
- candidates.jsonl: {count_jsonl(candidates)}
- shortlist.jsonl: {count_jsonl(shortlist)}
- references.bib: {bool(refs)}
- experiment_plan.md: {bool(experiment_plan)}
- paper.tex/main.tex: {bool(paper_tex)}
- paper.pdf: {bool(paper_pdf)}

## Status

`{idea_entry["status"]}`

## Failure markers

{failure_text}

## Notes

Add manual notes here:
- What worked:
- What failed:
- Next action:
""",
        encoding="utf-8",
    )

    print(f"Extracted run: {run_id}")
    print("Wrote registry: registries/idea_registry.jsonl")
    print(f"Wrote report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
