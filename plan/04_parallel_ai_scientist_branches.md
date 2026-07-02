# Parallel AI Scientist Branches

## Goal
Run AI Scientist v1 and v2 as sidecar experiment and idea-exploration branches after ARC produces enough planning artifacts.

## Inputs
- ARC scoped problem, literature synthesis, hypotheses, and experiment plan.
- AI Scientist v1 template requirements from `SakanaAI/AI-Scientist`.
- AI Scientist v2 workshop markdown and BFTS requirements from `SakanaAI/AI-Scientist-v2`.
- Model, compute, and safety settings.
- Existing AI Scientist run artifacts for v0 import-only mode.

## Outputs
- AI Scientist v1 import summary and optional synthetic template plan.
- AI Scientist v2 import summary and optional workshop/idea plan.
- Branch PDFs, logs, reviews, experiment results, token tracking, and summaries when available.
- Evidence contributions back to the registry.

## Agent Owner
Agent 4: AI Scientist.

## Instructions
- Treat both AI Scientist systems as sidecar branches, not replacement orchestrators.
- Disable live AI Scientist v1/v2 execution in v0 by default:
  - `ai_scientist_v1.enabled: false`
  - `ai_scientist_v2.enabled: false`
  - `import_existing_runs_only: true`
- Use v1 when ARC artifacts can synthesize a concrete experiment template.
- Use v2 when ARC artifacts can seed open-ended idea exploration and BFTS.
- Run v1 only when the topic matches an existing template, a baseline run is available, and the experiment can run in a controlled container.
- Run v2 only when ARC novelty is weak, multiple plausible hypotheses need exploration, review flags experiment direction, and compute budget allows it.
- Skip both branches when ARC quality gates pass, internal review has no blocking/high weaknesses, citation and claim gates pass, compute is low, or Docker/GPU requirements are unmet.
- Map AI Scientist model use through bridge aliases: `research_code`, `research_strong`, `research_review`, `research_citation`, and `research_fast`.
- Run branch execution under the agreed sandbox policy for generated code.
- Return branch evidence to ARC/registry flow without overwriting ARC mainline results.

## Acceptance Criteria
- v0 imports existing branch artifacts only; live runs require later manual approval and sandbox readiness.
- v1 and v2 branch plans are independently resumable when enabled.
- Branch outputs are normalized as sidecar evidence.
- Missing PDFs, skipped reviews, or failed experiments are represented explicitly.
- Branch results can support claim/evidence checks and internal review.

## Handoffs
- Receive ARC planning artifacts from Agent 2 and indexed paths from Agent 5.
- Hand branch evidence, logs, reviews, and PDFs to Agent 5.
- Hand branch review signals and weaknesses to Agent 6.
- Hand branch summary and unresolved issues to Agent 1.
