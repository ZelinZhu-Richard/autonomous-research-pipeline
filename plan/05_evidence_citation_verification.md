# Evidence and Citation Verification

## Goal
Verify claims, experiments, references, and inline citations before manuscript and external review stages rely on them.

## Inputs
- ARC paper drafts, experiment outputs, and bibliography artifacts.
- AI Scientist branch evidence and reviews.
- Existing claim, experiment, and citation registries.
- Optional future literature/citation helper outputs from paper-qa and gpt_academic.

## Outputs
- Claim-to-evidence mapping.
- Provisional, verified, and frozen citation registry states.
- Reference and inline-citation mismatch reports.
- Evidence gaps routed to revision or rerun.

## Agent Owner
Agent 5: Evidence + Citation.

## Instructions
- Extract citations after any bibliography-producing stage.
- Use ARC citation verification or equivalent local checks when verified references are available.
- Treat paper-qa and gpt_academic as optional future helper checks only; they are skipped in v0.
- Mandatory citation truth in v0 comes from the bridge citation registry, source registry, ARC verification report, and deterministic validators.
- Apply globally: hallucinated citations = 0, claim strength must not exceed evidence strength, major claims need evidence, and each experiment must support a named claim.
- Apply DeepSeek survey/literature-heavy thresholds only in survey or literature-heavy mode, not empirical v0.
- Freeze citations only after final bibliography and inline citations reconcile.
- Block final export on unresolved critical citation or evidence gaps.

## Acceptance Criteria
- Claims map to supporting experiment, branch, or literature artifacts.
- Citation state is clearly provisional, verified, or frozen.
- Duplicate, missing, hallucinated, or unresolved cite keys are surfaced.
- Frozen citation registry is ready for PaperReview.ai and final export.

## Handoffs
- Receive ARC and branch artifacts from Agents 2 and 4.
- Hand evidence gaps to Agent 6 for targeted revision.
- Hand frozen citation state to Agent 6 for PaperReview.ai and export.
- Hand audit summary to Agent 1.
