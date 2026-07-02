---
name: paper-writing-orchestrator
description: Routes paper-writing work across literature, structure, experiment, figures, and review loops for NeurIPS-style empirical papers.
metadata:
  category: writing
  trigger-keywords: "paper,manuscript,writing,revision,weakness,routing,quality,review,neurips,stall,loop,orchestrator"
  applicable-stages: "15,16,17,18,19,20"
  priority: "1"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from Scientific Paper Writing Skill Group: https://victorchen96.github.io/auto_research/skill/paper-writing.html"
---

## Purpose

Use this skill as the manuscript-level router. It coordinates five responsibilities:
literature coverage, paper structure, empirical support, figures/tables, and review
response. The default target is a NeurIPS-compatible empirical paper, not a pure
survey.

For long unattended runs, pair this skill with `deli-autoresearch-protocol` so
iteration state, stalled directions, and review loops are tracked in files rather
than conversation memory.

## Routing Rules

1. Citation coverage, missing recent work, weak venue quality, or unverified references route to `paper-literature-survey`.
2. Unclear thesis, weak taxonomy, missing gap, over-strong claims, or poor transitions route to `paper-structure-logic`.
3. Unsupported empirical claims, weak baselines, missing ablations, or unclear statistics route to `paper-experiment-design`.
4. Incomparable tables, missing error bars, weak captions, or unreferenced visuals route to `paper-figures-tables`.
5. Review scoring, weakness prioritization, regression checks, and final gate readiness route to `paper-peer-review-simulation`.

## Phase Loop

1. Draft: create a coherent skeleton, introduction, related work, and experiment plan.
2. Evidence: collect and verify citations, run or import empirical results, and bind claims to evidence.
3. Presentation: integrate results through compact tables, figures, and concise prose.
4. Review: simulate reviewers, route weaknesses, revise, and check for regressions.
5. Stop only when the paper has clear contribution claims, verified citations, defensible experiments, referenced figures/tables, and no blocking review weakness.

## Long-Horizon Controls

- Write major manuscript decisions and unresolved weaknesses to durable artifacts.
- Track repeated review failures as stalls, not as ordinary revision requests.
- After two rounds without material improvement, change the structure of the attempt: claim scope, evidence source, experiment design, or paper organization.
- Use independent review or verification passes for evidence chains and citation claims.

## Quality Policy

- Claim strength must never exceed evidence strength.
- A weakness is not fixed until the manuscript artifact changes and the review check no longer flags it.
- Survey-oriented thresholds from the source guidance are reference targets only. For this empirical pipeline, prioritize verified citations, experiment rigor, and NeurIPS reviewer expectations.
- Do not let a polished narrative hide missing evidence. Route back to the responsible sub-skill.
