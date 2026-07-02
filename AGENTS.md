Autonomous Research Pipeline Specifics

Purpose:
Build a NeurIPS-compatible empirical autonomous research pipeline with AutoResearchClaw as the main spine, MetaClaw as the skill/memory layer, AI Scientist v1/v2 as optional sidecar imports, DeepSeek-style skill guidance as policy/check material, and PaperReview.ai as a manual final external gate.

Read order for autonomous agents:

1. Read this `AGENTS.md`.
2. Read `project/README.md`.
3. Read `plan/00_pipeline_and_agents.md`.
4. Read `project/component_map.md`.
5. Read your assigned `project/agents/*.md` role brief and `project/components/*.md` component file.
6. Check `plan/q.md` for answered decisions and remaining unresolved items.

Non-negotiable v0 defaults:

- Target venue: NeurIPS-compatible.
- Paper type: empirical.
- Seed topic: Robust Citation and Review-Gate Feedback Loops for Autonomous Research Agents.
- AutoResearchClaw is the primary execution spine.
- MetaClaw starts in `skills_only` mode; do not start with RL mode.
- AI Scientist v1/v2 live runs are disabled by default; import existing artifacts only unless later manually approved.
- External skill repositories do not execute code in v0.
- Repo-local `skills/` is canonical. User-level MetaClaw skills are generated exports only.
- Generated-code execution requires Docker or an equivalent sandbox. Never run LLM-generated experiment code directly on the host.

Runtime model:

- The pipeline is CLI-first. One operator should be able to run it from command line targets once implementation exists.
- Multi-agent coordination is preferred for parallel development, review, and auditing, but it is not required to run v0.
- If working alone, follow the same plan order and treat the six agents as responsibility labels.

Allowed write paths for planning work:

- `plan/`
- `project/`
- `skills/`
- `external/LOCKFILE.md`
- `external/LOCKFILE.json`

Implementation work should stay in the existing source/config/registry/report folders unless a plan explicitly says otherwise.

1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

State your assumptions explicitly. If uncertain, ask.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
If something is unclear, stop. Name what's confusing. Ask.
2. Simplicity First
Minimum code that solves the problem. Nothing speculative.

No features beyond what was asked.
No abstractions for single-use code.
No "flexibility" or "configurability" that wasn't requested.
No error handling for impossible scenarios.
If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes
Touch only what you must. Clean up only your own mess.

When editing existing code:

Don't "improve" adjacent code, comments, or formatting.
Don't refactor things that aren't broken.
Match existing style, even if you'd do it differently.
If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:

Remove imports/variables/functions that YOUR changes made unused.
Don't remove pre-existing dead code unless asked.
The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution
Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

"Add validation" → "Write tests for invalid inputs, then make them pass"
"Fix the bug" → "Write a test that reproduces it, then make it pass"
"Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
