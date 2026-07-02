# MetaClaw Skills Component

## Canonical Stage Links
- `../../plan/01_arc_metaclaw_spine.md`
- `../../plan/02_skill_policy_stack.md`
- `../../plan/06_manuscript_build_and_skill_checks.md`

## Ownership
Own DeepSeek policy compilation, bridge skill packets, and MetaClaw skill synchronization.

## Responsibilities
- Compile DeepSeek-style paper-writing guidance into quality profiles and skill packets.
- Render bridge-owned `SKILL.md` files for MetaClaw, ARC, and Codex-facing skill directories.
- Produce bridge validator checklists from the same guidance.
- Probe MetaClaw health and report ready, degraded, or down states.
- Preserve non-bridge MetaClaw skills.

## Interfaces
- Inputs: NeurIPS empirical profile, DeepSeek-style policy text, skill packet contract, weakness routing policy, MetaClaw config.
- Outputs: skill packets, rendered skill files, validator checklists, MetaClaw health status, routing policy artifacts.
- Consumers: validators, review weakness router, LLM proxy setup, and cross-run learning flows.

## Parallelization Notes
- Can proceed in parallel with ARC once contracts are stable.
- Coordinate with review routing before changing weakness category names.
- Coordinate with security before enabling any executable tool path.
- In v0, do not execute external skill repository code.

## Acceptance Criteria
- Generated skills are namespaced and repeatable.
- Proxy-down state degrades cleanly when direct LLM fallback is available.
- Survey thresholds are not applied outside survey mode by default.
- Existing MetaClaw skills are not overwritten.
- Repo-local `skills/` remains canonical; user-level `~/.metaclaw/skills` is updated only by explicit export command.

## Open Questions
- What exact MetaClaw `SKILL.md` header format should be used for the installed version?
- Which generated skill export command should write `.agents/skills/`, `.claude/skills/`, and `~/.metaclaw/skills/`?
