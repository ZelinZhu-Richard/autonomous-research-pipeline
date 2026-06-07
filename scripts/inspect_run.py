from __future__ import annotations

import json
import sys
from pathlib import Path


IMPORTANT_NAMES = {
    "goal.md",
    "problem_tree.md",
    "search_plan.yaml",
    "sources.json",
    "queries.json",
    "candidates.jsonl",
    "shortlist.jsonl",
    "references.bib",
    "experiment_plan.md",
    "paper.tex",
    "main.tex",
    "paper.pdf",
}


def count_jsonl(path: Path) -> int:
    try:
        return sum(1 for line in path.read_text(errors="ignore").splitlines() if line.strip())
    except Exception:
        return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/inspect_run.py <run_dir>")
        return 1

    run_dir = Path(sys.argv[1]).expanduser().resolve()

    if not run_dir.exists():
        print(f"Run directory not found: {run_dir}")
        return 1

    print(f"Run directory: {run_dir}")
    print()

    files = sorted([p for p in run_dir.rglob("*") if p.is_file()])
    print(f"Total files: {len(files)}")
    print()

    print("Important artifacts:")
    found_any = False
    for p in files:
        if p.name in IMPORTANT_NAMES:
            found_any = True
            rel = p.relative_to(run_dir)
            extra = ""
            if p.suffix == ".jsonl":
                extra = f" ({count_jsonl(p)} lines)"
            print(f"  ✅ {rel}{extra}")

    if not found_any:
        print("  No common important artifacts found yet.")

    print()
    print("Top-level tree:")
    for p in sorted(run_dir.iterdir()):
        icon = "📁" if p.is_dir() else "📄"
        print(f"  {icon} {p.name}")

    print()
    print("Next checks:")
    print("  1. Did shortlist.jsonl exist?")
    print("  2. Did experiment_plan.md exist?")
    print("  3. Did references.bib exist?")
    print("  4. Did any stage fail before EXPERIMENT_DESIGN?")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
