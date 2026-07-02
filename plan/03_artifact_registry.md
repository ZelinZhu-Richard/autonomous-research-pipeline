# Artifact Registry

## Goal
Normalize outputs from ARC, MetaClaw, AI Scientist side branches, citation tools, reviews, and export steps into shared registries.

## Inputs
- ARC run artifacts from Agent 2.
- MetaClaw skill and lesson artifacts.
- AI Scientist branch outputs from Agent 4.
- Claim, experiment, citation, review, and package artifacts from Agents 5 and 6.

## Outputs
- Updated run, idea, experiment, claim, citation, and review registries.
- Run cards and leaderboard inputs.
- Artifact index with source system, role, path, hash, and provenance.
- Handoff-ready summaries for downstream agents.

## Agent Owner
Agent 5: Evidence + Citation.

## Instructions
- Normalize artifacts before validators or reviewers consume them.
- Keep ARC mainline artifacts separate from sidecar evidence.
- Prefer JSONL registries for incremental updates when consistent with existing `registries/`.
- Record artifact provenance so final package consumers can trace claims back to source runs.
- Do not let agents read upstream folders ad hoc when the registry has a normalized entry.

## Acceptance Criteria
- ARC and branch artifacts are indexed with source system and role.
- Claims, experiments, citations, reviews, and run cards have registry locations.
- Missing artifacts produce explicit gaps, not silent omissions.
- Downstream agents can consume registry entries without guessing paths.

## Handoffs
- Hand indexed ARC planning artifacts to Agent 4.
- Hand paper, claim, experiment, and citation entries to Agent 5 validation tasks.
- Hand reviewable draft and artifact index to Agent 6.
- Hand final registry snapshots to Agent 1.
