# PaperReview and Export Component

## Canonical Stage Links
- `../../plan/07_internal_review_and_revision_loop.md`
- `../../plan/08_paperreview_external_gate.md`
- `../../plan/09_final_audited_package.md`

## Ownership
Own external release-candidate review preparation and final export packaging.

## Responsibilities
- Prepare PaperReview.ai manual submission packet.
- Always generate or reference `paperreview_first15.pdf`.
- Import returned PaperReview.ai review artifacts and hand them to review normalization.
- Assemble final export bundle with paper, manifests, citations, reviews, validator results, and summary.

## Interfaces
- Inputs: final PDF, frozen citation registry, NeurIPS venue/profile, `PAPERREVIEW_EMAIL`, review import artifact, validation results.
- Outputs: review submission packet, `paperreview_first15.pdf`, imported raw review reference, normalized review packet candidate, final export bundle.
- Consumers: release gate, user-facing final package, review weakness router.

## Parallelization Notes
- Export layout can be planned before PaperReview.ai is available.
- External review import can use saved HTML/JSON fixtures.
- Coordinate with citations before consuming frozen registry paths.
- Submission remains manual in v0.

## Acceptance Criteria
- Release-candidate packet includes PDF, venue, email, and frozen citation registry reference.
- External review waiting state is explicit and resumable.
- Final bundle includes all required artifacts with hashes or stable references.
- Bundle inspection does not require guessing upstream run directories.
- PaperReview.ai submission is blocked unless internal review score is at least 6.5/10 and no blocking issues remain.

## Open Questions
- What local `.env.local` value should be used for `PAPERREVIEW_EMAIL`?
- Should `make package-full` be added for self-contained archives after the default reference-by-hash package works?
