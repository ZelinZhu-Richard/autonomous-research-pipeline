# Reviews and Weakness Router Component

## Canonical Stage Links
- `../../plan/06_manuscript_build_and_skill_checks.md`
- `../../plan/07_internal_review_and_revision_loop.md`
- `../../plan/08_paperreview_external_gate.md`
- `../../plan/09_final_audited_package.md`

## Ownership
Own review normalization and weakness-to-remediation routing.

## Responsibilities
- Normalize ARC, AI Scientist, DeepSeek-style, and PaperReview.ai reviews into review packets.
- Preserve source-specific scores while exposing shared strengths, weaknesses, and action items.
- Route weaknesses to remediation stages, validators, or skill packet generation.
- Detect parse loss, unsupported score maps, and unroutable weakness categories.

## Interfaces
- Inputs: raw review artifacts, target artifact IDs, venue/profile, routing table, skill packet contract.
- Outputs: normalized review packets, weakness routing decisions, action item queues, unresolved mapping reports.
- Consumers: MetaClaw skills, citation/claim validators, export readiness, lead orchestration.

## Parallelization Notes
- Build review fixtures independently of live adapters.
- Coordinate with PaperReview export for external review import shape.
- Coordinate with MetaClaw before converting recurring weaknesses into skills.

## Acceptance Criteria
- At least one fixture per review source normalizes cleanly or fails with clear parse errors.
- Every extracted weakness is routed, deferred, or marked unresolved.
- Critical citation, evidence, or security weaknesses block release.
- Raw review references remain auditable.

## Open Questions
- What severity thresholds should trigger blocking versus advisory findings?
- Should conflicting reviewer recommendations be merged automatically or escalated?
