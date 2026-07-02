# Citations and Claims Component

## Canonical Stage Links
- `../../plan/03_artifact_registry.md`
- `../../plan/05_evidence_citation_verification.md`
- `../../plan/08_paperreview_external_gate.md`
- `../../plan/09_final_audited_package.md`

## Ownership
Own citation registry lifecycle and claim/evidence validation.

## Responsibilities
- Extract provisional citation registry after draft bibliography-producing stages.
- Import or run verification to produce verified citation state.
- Freeze the citation registry for review and export consumers.
- Connect paper claims to experiment or branch evidence where available.
- Enforce v0 global gates: no hallucinated citations, claim strength not exceeding evidence strength, major claims requiring evidence, and each experiment supporting a named claim.

## Interfaces
- Inputs: bibliography files, inline citation-bearing drafts, ARC verification reports, branch paper artifacts, claim registry, deterministic validator outputs.
- Outputs: provisional, verified, and frozen citation registries; citation validator findings; claim evidence findings.
- Consumers: PaperReview.ai packet preparation, export bundle, release gate, review router.

## Parallelization Notes
- Provisional extraction can start as soon as ARC import exposes bibliography artifacts.
- Claim/evidence checks can proceed with fixtures while verification is still being finalized.
- Coordinate with export before changing frozen registry filenames or roles.
- paper-qa and gpt_academic are optional future helpers only; they are skipped in v0.

## Acceptance Criteria
- Citation registry statuses remain distinct: provisional, verified, frozen.
- Duplicate, missing, or unresolved cite keys are deterministic failures.
- Frozen citations are immutable unless verification is reopened.
- Claim/evidence fixtures include one happy path and one adversarial path.
- Survey/literature-heavy thresholds are not applied to empirical v0.

## Open Questions
- Should claim extraction use existing `scripts/extract_claims.py` as-is or become part of bridge validators?
- What citation metadata checks require network access versus local-only validation?
