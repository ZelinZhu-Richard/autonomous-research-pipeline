# Pipeline and Agents

## Goal
Define the end-to-end research pipeline and the six-agent execution model for building faster without turning every upstream system into a competing orchestrator.

## Inputs
- `structure_v2.md` as the architecture reference.
- AutoResearchClaw as the primary research spine.
- MetaClaw as the memory, skill, and proxy layer.
- AI Scientist v1 and v2 as parallel sidecar experiment branches.
- DeepSeek paper-writing guidance as the v0 skill-policy source.
- Deferred external research-skill repositories as later policy/check sources.
- PaperReview.ai as the external release-candidate verification gate.

## Outputs
- A single ordered pipeline from ARC setup to final audited package.
- A CLI-first runtime model that can run the pipeline without spawning multiple autonomous agents.
- A six-agent ownership model with handoffs and concurrency rules.
- A shared expectation that plan files are pipeline checkpoints, not independent orchestrators.

## Agent Owner
Agent 1: Lead/Integrator.

## Instructions
- Runtime rule: the pipeline should be runnable from the command line as one orchestrated workflow. Multi-agent coordination is not required to run v0.
- Use agents as a development and review acceleration model, not as a hard runtime dependency.
- Prefer the six-agent split when multiple humans/agents are building or auditing the project in parallel:
  - Agent 1: Lead/Integrator owns pipeline state, handoffs, final package, and this file.
  - Agent 2: ARC + MetaClaw owns ARC execution/import and MetaClaw skill sync.
  - Agent 3: Skill Policy owns DeepSeek-derived policy, validator checklists, and generated skills.
  - Agent 4: AI Scientist owns v1/v2 sidecar branch setup, import, and summaries.
  - Agent 5: Evidence + Citation owns registries, claims, citations, and deterministic validation.
  - Agent 6: Review + Export owns internal review, PaperReview.ai, and release packaging.
- Start Agents 2, 3, and 5 first.
- Start Agent 4 after ARC produces planning, hypothesis, or experiment artifacts.
- Start Agent 6 after a compiled or reviewable draft exists.
- Agent 1 runs throughout to merge outputs, update handoffs, and resolve conflicts.
- Treat ARC as the master spine; all other systems contribute evidence, checks, or review signal.
- If one operator is running the project alone, follow the same pipeline order and treat the agent names as responsibility labels.
- Use NeurIPS-compatible empirical mode as the v0 default.
- Use the seed topic `Robust Citation and Review-Gate Feedback Loops for Autonomous Research Agents`.
- Keep AI Scientist v1/v2 live execution disabled in v0; import existing branch artifacts only unless manually approved later.
- Do not execute external skill repositories in v0. Skills guide behavior; validators decide pass/fail.

## Acceptance Criteria
- The pipeline uses ARC + MetaClaw as the main execution path.
- The pipeline can be run from command line without requiring multiple live agents.
- AI Scientist v1/v2 are explicitly sidecar branches.
- Skill repositories are classified as policy/check sources unless a safer executable interface is confirmed.
- PaperReview.ai is the final external gate, not an inner-loop executor.
- Six preferred development roles are listed with clear ownership and concurrency rules.
- v0 defaults are explicit: NeurIPS-compatible, empirical, import-only AI Scientist branches, no external skill execution.

## Handoffs
- Agent 1 hands ARC-ready requirements to Agent 2.
- Agent 2 hands ARC artifacts to Agents 4 and 5.
- Agent 3 hands policy checklists to Agents 2, 5, and 6.
- Agent 4 hands branch results to Agents 5 and 6.
- Agent 5 hands frozen evidence/citation state to Agent 6.
- Agent 6 hands the audited package back to Agent 1 for final signoff.
