# Skill Policy Stack

## Goal
Compile v0 skill guidance into robustness checks, writing guidance, generated skills, and validator checklists without turning external skill repositories into executable dependencies.

## Inputs
- DeepSeek-style paper-writing guidance.
- Deferred skill repositories for later policy review, not v0 execution:
  - `brycewang-stanford/Auto-Empirical-Research-Skills`
  - `Imbad0202/academic-research-skills`
  - `Orchestra-Research/AI-Research-SKILLs`
  - `Imbad0202/academic-research-skills-codex`
  - `Norman-bury/research-writing-skill`
  - `Master-cai/Research-Paper-Writing-Skills`
  - `WUBING2023/PaperSpine`
  - `Yuan1z0825/nature-skills`
- Literature/citation helpers:
  - `binary-husky/gpt_academic`
  - `Future-House/paper-qa`

## Outputs
- Policy checklist for literature, experiment design, paper structure, figures/tables, and review simulation.
- MetaClaw skill packets or `SKILL.md` render inputs.
- ARC/Codex-compatible skill exports when needed.
- Bridge validator checklists that decide pass/fail independently from skill text.
- Writing and robustness gates for manuscript build and internal review.
- Tool classification table with v0 enabled, v0 skipped, and future candidates.

## Agent Owner
Agent 3: Skill Policy.

## Instructions
- Use only DeepSeek-style paper-writing guidance as v0 policy text.
- Skip nonessential external skill repositories in v0, including gpt_academic, paper-qa, A-Evolve, untrusted community skills, and random external skill repos.
- Keep the deferred repositories classified for later review:
  - Core writing/quality candidates: PaperSpine, research-writing-skill, Research-Paper-Writing-Skills, and nature-skills.
  - Research/experiment candidates: Auto-Empirical-Research-Skills, AI-Research-SKILLs, academic-research-skills, and academic-research-skills-codex.
  - Literature/citation helper candidates: paper-qa and gpt_academic.
- Convert skill guidance into explicit checks for ARC, AI Scientist outputs, citations, manuscript structure, and review readiness.
- Convert guidance into both generated skills and bridge validator checklists.
- Treat repo-local `skills/` as canonical. `.agents/skills/`, `.claude/skills/`, and `~/.metaclaw/skills/` are generated exports.
- Never silently mutate `~/.metaclaw/skills` during tests; require an explicit export command.
- Do not execute external skill repositories in v0.

## Acceptance Criteria
- Every listed repo is assigned to v0 enabled, v0 skipped, or future candidate status.
- DeepSeek's five sub-skills are represented as checks: literature survey, paper structure/logic, experiment design, figures/tables, and peer review simulation.
- Survey-specific thresholds are not applied to non-survey work without explicit profile selection.
- MetaClaw, ARC, and Codex can consume generated skills, while bridge validators provide pass/fail enforcement.

## Handoffs
- Hand ARC-stage skill guidance to Agent 2.
- Hand evidence and citation checks to Agent 5.
- Hand manuscript and review checks to Agent 6.
- Hand skill packet summaries to Agent 1 for final audit records.
