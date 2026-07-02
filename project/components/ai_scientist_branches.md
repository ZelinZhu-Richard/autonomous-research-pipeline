# AI Scientist Branches Component

## Canonical Stage Links
- `../../plan/04_parallel_ai_scientist_branches.md`
- `../../plan/05_evidence_citation_verification.md`
- `../../plan/07_internal_review_and_revision_loop.md`

## Ownership
Own AI Scientist v1 and v2 side-branch generation, execution/import, and artifact normalization.

## Responsibilities
- Synthesize AI Scientist v1 templates from ARC artifacts.
- Generate AI Scientist v2 workshop markdown and idea JSON from ARC artifacts.
- Import v1 and v2 results as branch evidence, not as replacements for ARC mainline artifacts.
- Normalize branch PDFs, reviews, logs, ideas, token tracking, and result artifacts.

## Interfaces
- Inputs: ARC problem, synthesis, hypothesis, experiment plan, bridge model aliases, existing branch artifacts for v0.
- Outputs: branch manifests, optional template/workshop plans, imported artifacts, review packet candidates.
- Consumers: evidence validators, review normalization, weakness router, and final export.

## Parallelization Notes
- Importer and fixture work can proceed before live GPU execution.
- v1 and v2 lanes can be assigned to separate agents if contract names are stable.
- Coordinate with security before running generated code.
- In v0, import existing AI Scientist artifacts only; live runs default to zero.

## Acceptance Criteria
- v1 import fixture normalizes notes, logs, PDF, and review outputs when present.
- v2 import fixture normalizes idea files, token trackers, PDFs, logs, and review outputs when present.
- Missing PDF or skipped review is represented as an event rather than hidden.
- Branch outputs remain clearly marked as sidecar evidence.
- Live branch execution remains disabled until sandbox readiness and manual approval are recorded.

## Open Questions
- Which existing AI Scientist artifacts should be used as the first import fixtures?
- Which v1 template, if any, is CPU-feasible for a later live smoke test?
