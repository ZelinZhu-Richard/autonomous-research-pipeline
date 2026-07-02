# Component Map

This map keeps the `../plan/` pipeline files canonical while assigning implementation ownership by agent/component.

| Canonical pipeline file | Primary owner | Supporting owners |
| --- | --- | --- |
| `../plan/00_pipeline_and_agents.md` | Agent 1: Lead/Integrator | All agents |
| `../plan/01_arc_metaclaw_spine.md` | Agent 2: ARC + MetaClaw | Agent 3, Agent 5 |
| `../plan/02_skill_policy_stack.md` | Agent 3: Skill Policy | Agent 2, Agent 5, Agent 6 |
| `../plan/03_artifact_registry.md` | Agent 5: Evidence + Citation | Agent 1, Agent 2, Agent 4, Agent 6 |
| `../plan/04_parallel_ai_scientist_branches.md` | Agent 4: AI Scientist | Agent 2, Agent 5, Agent 6 |
| `../plan/05_evidence_citation_verification.md` | Agent 5: Evidence + Citation | Agent 2, Agent 4, Agent 6 |
| `../plan/06_manuscript_build_and_skill_checks.md` | Agent 6: Review + Export | Agent 3, Agent 5 |
| `../plan/07_internal_review_and_revision_loop.md` | Agent 6: Review + Export | Agent 2, Agent 4, Agent 5 |
| `../plan/08_paperreview_external_gate.md` | Agent 6: Review + Export | Agent 1, Agent 5 |
| `../plan/09_final_audited_package.md` | Agent 1: Lead/Integrator | Agent 6 |

## Parallel Work Lanes
- Agent 1 runs throughout and owns pipeline state, handoffs, and final signoff.
- Agents 2, 3, and 5 start first.
- Agent 4 starts after ARC produces planning, hypothesis, or experiment artifacts.
- Agent 6 starts after a compiled or reviewable manuscript draft exists.
- ARC remains the main spine; AI Scientist outputs are sidecar evidence; v0 imports AI Scientist artifacts only; external skill repos provide policy/checks and do not execute code.
