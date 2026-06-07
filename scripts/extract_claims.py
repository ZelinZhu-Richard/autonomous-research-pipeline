from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CLAIM_TRIGGERS = [
    "outperform",
    "improve",
    "increase",
    "reduce",
    "decrease",
    "achieve",
    "show",
    "demonstrate",
    "suggest",
    "indicate",
    "results",
    "performance",
    "robust",
    "failure",
    "better",
    "worse",
    "significant",
    "effective",
    "efficient",
    "accurate",
    "state-of-the-art",
    "sota",
]


EMPIRICAL_TRIGGERS = [
    "outperform",
    "improve",
    "increase",
    "reduce",
    "decrease",
    "achieve",
    "results",
    "performance",
    "accuracy",
    "recall",
    "mrr",
    "precision",
    "f1",
    "auc",
    "%",
]


def find_first(run_dir: Path, names: list[str]) -> Path | None:
    for name in names:
        matches = list(run_dir.rglob(name))
        if matches:
            return matches[0]
    return None


def strip_latex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\begin\{[^}]+\}", " ", text)
    text = re.sub(r"\\end\{[^}]+\}", " ", text)
    text = re.sub(r"\\section\{([^}]*)\}", r"\1. ", text)
    text = re.sub(r"\\subsection\{([^}]*)\}", r"\1. ", text)
    text = re.sub(r"\\subsubsection\{([^}]*)\}", r"\1. ", text)
    text = re.sub(r"\\textbf\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    raw = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in raw if len(s.strip()) > 40]


def citation_keys(sentence: str) -> list[str]:
    keys = []
    for match in re.findall(r"\\cite[t|p|alp|author|year]*\{([^}]+)\}", sentence):
        keys.extend([k.strip() for k in match.split(",") if k.strip()])
    return keys


def classify_claim(sentence: str) -> str:
    s = sentence.lower()

    if "\\cite" in sentence:
        return "literature"

    if any(t in s for t in EMPIRICAL_TRIGGERS):
        return "empirical"

    if "we propose" in s or "we introduce" in s or "our method" in s:
        return "method"

    return "general"


def evidence_status(sentence: str, claim_type: str, keys: list[str]) -> str:
    if keys:
        return "citation_present"

    if claim_type == "empirical":
        return "needs_experiment_evidence"

    if claim_type == "literature":
        return "needs_citation"

    return "needs_manual_review"


def likely_claim(sentence: str) -> bool:
    s = sentence.lower()
    return any(t in s for t in CLAIM_TRIGGERS)


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
            pass
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/extract_claims.py <run_dir> <run_id>")
        return 1

    run_dir = Path(sys.argv[1]).expanduser().resolve()
    run_id = sys.argv[2]

    if not run_dir.exists():
        print(f"Run directory not found: {run_dir}")
        return 1

    paper = find_first(
        run_dir,
        [
            "paper.tex",
            "main.tex",
            "draft.tex",
            "paper.md",
            "manuscript.tex",
            "report.md",
        ],
    )

    registry_path = Path("registries/claim_registry.jsonl")
    existing = load_jsonl(registry_path)
    existing = [row for row in existing if row.get("run_id") != run_id]

    if not paper:
        write_jsonl(registry_path, existing)
        print(f"No paper file found in {run_dir}. No claims extracted.")
        return 0

    raw = paper.read_text(errors="ignore")
    clean = strip_latex(raw)
    sentences = split_sentences(clean)

    rows = []
    now = datetime.now(timezone.utc).isoformat()

    claim_index = 1
    for sentence in sentences:
        if not likely_claim(sentence):
            continue

        keys = citation_keys(sentence)
        claim_type = classify_claim(sentence)

        rows.append(
            {
                "claim_id": f"{run_id}_claim_{claim_index:04d}",
                "run_id": run_id,
                "source_file": str(paper.relative_to(run_dir)),
                "created_at": now,
                "claim_text": sentence,
                "claim_type": claim_type,
                "citation_keys": keys,
                "evidence_status": evidence_status(sentence, claim_type, keys),
                "verified": False,
                "notes": "",
            }
        )
        claim_index += 1

    write_jsonl(registry_path, existing + rows)

    report_dir = Path("reports/claim_cards")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{run_id}_claims.md"

    needs_evidence = [r for r in rows if r["evidence_status"] != "citation_present"]

    report_lines = [
        f"# Claim Card: {run_id}",
        "",
        f"Source paper: `{paper}`",
        "",
        f"Total extracted claims: {len(rows)}",
        f"Claims needing evidence/manual review: {len(needs_evidence)}",
        "",
        "## Claims needing review",
        "",
    ]

    for row in needs_evidence[:50]:
        report_lines += [
            f"### {row['claim_id']}",
            "",
            f"Type: `{row['claim_type']}`",
            f"Evidence status: `{row['evidence_status']}`",
            "",
            row["claim_text"],
            "",
        ]

    if not needs_evidence:
        report_lines.append("No unsupported claims detected by heuristic extractor.")

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Extracted {len(rows)} claims from {paper.name}")
    print(f"Wrote registry: {registry_path}")
    print(f"Wrote report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())