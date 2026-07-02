# Multi-Agent Project Workspace

This folder is the coordination workspace for parallel agents working on the AutoResearchClaw, MetaClaw, AI Scientist, DeepSeek policy, PaperReview.ai bridge.

The canonical stage plan remains in `../plan/`. The files in this folder reorganize that stage plan by implementation component so multiple agents can work at the same time without duplicating the source plan.

## How Agents Work Here
- If you are running the pipeline from the command line, you do not need to spawn multiple agents. Use the pipeline docs as ordered operating instructions.
- If you are building, auditing, or parallelizing work, use the six-agent split as responsibility labels.
- Read `../AGENTS.md` first for repo-wide operating rules.
- Read `../plan/00_pipeline_and_agents.md` for the pipeline and six-agent concurrency model.
- Read `component_map.md` to understand which component owns which pipeline files.
- Pick one component from `components/` and one role brief from `agents/`.
- Before starting, add an entry to `coordination/status_board.md`.
- During work, write short updates in `coordination/messages.md`.
- Put durable architecture decisions in `coordination/decisions.md`.
- Put handoff notes in `coordination/handoffs.md`.
- Put blocked work in `coordination/blockers.md`.

## Agent Read Locations
- Root instructions: `../AGENTS.md`.
- Canonical pipeline plan: `../plan/00_pipeline_and_agents.md` through `../plan/09_final_audited_package.md`.
- Open decisions: `../plan/q.md`.
- Current v0 decisions: NeurIPS-compatible empirical mode, ARC as main spine, MetaClaw `skills_only`, AI Scientist import-only, no external skill execution, PaperReview.ai manual gate.
- Component ownership and coordination: this `project/` folder.
- Agent role briefs: `agents/`.
- Shared agent communication: `coordination/`.
- Repo-local skill material and generated bridge skills: `../skills/`.
- External upstream checkouts or references: `../external/`.
- Optional generated skill exports: `../.agents/skills/`, `../.claude/skills/`, and `~/.metaclaw/skills/` only via explicit export command.

## Component Ownership
- `components/contracts_core.md`: bridge contracts and stable schemas.
- `components/arc_primary.md`: AutoResearchClaw primary run/import adapter.
- `components/metaclaw_skills.md`: DeepSeek policy compilation and MetaClaw skill sync.
- `components/ai_scientist_branches.md`: AI Scientist v1 and v2 side branches.
- `components/citations_claims.md`: citation registry and claim/evidence checks.
- `components/reviews_weakness_router.md`: normalized reviews and weakness routing.
- `components/paperreview_export.md`: PaperReview.ai and final export bundle.
- `components/security_ci_fixtures.md`: sandboxing, CI, fixtures, and acceptance gates.

## Coordination Rules
- Do not move or duplicate `../plan/00_*.md` through `../plan/09_*.md`.
- Component files link back to canonical stage files and own subsystem-level planning.
- Agents coordinate through `coordination/` before changing overlapping implementation areas.
- If two agents need the same file, one agent owns the edit and the other leaves a handoff note.
- A component is ready for implementation only when its inputs, outputs, tests, and blockers are explicit.
- Do not run external skill repository code in v0.
- Do not run AI Scientist live branches in v0 unless the plan is changed and manual approval is recorded.

## Project Shape
Use this folder as an agent communication layer, not as runtime output. Source code, configs, fixtures, runs, registries, reports, and plans stay in the existing repo folders unless a later implementation plan changes that intentionally.
