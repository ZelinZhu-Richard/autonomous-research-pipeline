# PaperReview.ai External Gate

## Goal
Use PaperReview.ai as a final external verification gate for a serious release-candidate PDF.

## Inputs
- Release-candidate PDF.
- Frozen citation registry.
- Target venue `NeurIPS` for v0 and submission email from `PAPERREVIEW_EMAIL`.
- Internal review readiness decision.

## Outputs
- PaperReview.ai submission packet.
- Required `paperreview_first15.pdf` review-focused variant.
- Imported raw PaperReview.ai review when returned.
- Normalized external review packet and external-gate decision.

## Agent Owner
Agent 6: Review + Export.

## Instructions
- Preserve PaperReview.ai constraints: browser PDF upload, email notification, first 15 pages analyzed, and reviews may contain errors.
- Keep submission manual or semi-manual until a public API is confirmed.
- Do not hardcode email in source code. Read `PAPERREVIEW_EMAIL` from local environment when preparing metadata.
- Use `NeurIPS` as the v0 target venue when the final venue is undecided; use `Other` only for clearly non-ML future targets.
- Always generate `paperreview_first15.pdf`.
- Prepare the first 15 pages so they contain the abstract, strongest framing, method, results, limitations, and key references.
- Record manual submission metadata and import pasted or downloaded review text into `review_issue.json` and the normalized review packet format.
- Treat PaperReview.ai as an external signal, not as unquestioned truth.

## Acceptance Criteria
- Submission packet includes PDF path, `PAPERREVIEW_EMAIL`, `NeurIPS` target venue, and frozen citation reference.
- `paperreview_first15.pdf` exists for every external-gate attempt.
- Waiting-for-review state is explicit.
- Returned review can be imported and routed through the weakness router.
- External review issues are resolved, waived, or recorded before final packaging.

## Handoffs
- Receive release-candidate readiness from the internal review loop.
- Hand external weaknesses to Agent 6 revision routing and Agent 1 signoff.
- Hand imported external review packet to final package assembly.
