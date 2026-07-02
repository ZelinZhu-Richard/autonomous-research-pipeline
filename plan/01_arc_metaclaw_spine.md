# ARC MetaClaw Spine

## Goal
Use AutoResearchClaw as the master research pipeline and MetaClaw as the skill, memory, and proxy layer.

## Inputs
- Seed idea or research topic from `ideas/seed_ideas/`.
- ARC config from `configs/researchclaw.yaml`.
- MetaClaw skills/proxy configuration.
- Writing and research skill policies from the skill-policy stage.
- Model aliases from the bridge config: `research_default`, `research_strong`, `research_fast`, `research_code`, `research_review`, and `research_citation`.

## Outputs
- ARC run directory under `runs/raw/` or imported ARC run artifacts.
- ARC planning, literature, experiment, draft, review, quality, paper, and citation artifacts.
- MetaClaw skill updates and run lessons.
- Normalized run summary for registry and sidecar agents.

## Agent Owner
Agent 2: ARC + MetaClaw.

## Instructions
- Let ARC handle topic/profile intake, run configuration, staged execution, and resumability.
- Do not maintain a separate topic-intake stage unless ARC cannot express a required constraint.
- Use NeurIPS-compatible empirical mode for v0:
  - `target_venue: neurips`
  - `paperreview_target: NeurIPS`
  - `paper_type: empirical`
  - `domain_profile: general_ml_agents`
- Use the first full pipeline seed topic: `Robust Citation and Review-Gate Feedback Loops for Autonomous Research Agents`.
- Route default ARC calls through `research_default`; use `research_strong` for hypothesis generation, experiment design, code generation, result analysis, paper drafting, peer review, quality gates, and citation verification.
- Start MetaClaw in skills-only mode when available and route ARC LLM traffic through it when configured.
- Use `research_fast` for MetaClaw skill injection/summarization and `research_strong` for MetaClaw lesson synthesis.
- Do not start MetaClaw RL mode in v0.
- Sync bridge/writing skills into MetaClaw before ARC writing and review stages.
- Preserve ARC as the authoritative source for the mainline paper.
- Record layout drift between ARC `stage-*` artifacts and any `deliverables/` output.
- Require upstream pins in `external/LOCKFILE.json` and `external/LOCKFILE.md` before treating live upstream runs as reproducible.

## Acceptance Criteria
- ARC can run or import a research run using the configured seed idea.
- MetaClaw skill sync is attempted and degraded cleanly if the proxy is unavailable.
- ARC artifacts are discoverable for registry, AI Scientist, citation, and review agents.
- Topic/profile ownership is clearly inside ARC, not duplicated in another plan file.
- ARC does not hardcode provider names; it uses bridge model aliases.

## Handoffs
- Hand planning, synthesis, hypothesis, and experiment artifacts to Agent 4.
- Hand paper, bibliography, experiment, claim, and run-card artifacts to Agent 5.
- Hand draft/review/quality outputs to Agent 6.
- Hand new MetaClaw lessons to Agent 1 for final package inclusion.
