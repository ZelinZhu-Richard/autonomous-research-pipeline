---
name: paper-peer-review-simulation
description: Multi-persona peer review, score calibration, weakness routing, anti-inflation rules, and final quality gate checks.
metadata:
  category: writing
  trigger-keywords: "peer review,reviewer,score,weakness,quality gate,accept,reject,regression,major,minor"
  applicable-stages: "18,19,20"
  priority: "1"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from Scientific Paper Writing Skill Group: https://victorchen96.github.io/auto_research/skill/paper-writing.html"
---

## Purpose

Use this skill to simulate skeptical review and route fixes. The goal is not a
high score by assertion. The goal is a prioritized weakness list that drives
real manuscript changes.

## Reviewer Personas

Run three to five independent review perspectives:

1. Experimentalist: baselines, statistical rigor, replication, and ablations.
2. Theorist: definitions, formal claims, taxonomy consistency, and technical depth.
3. Perfectionist: prose clarity, formatting, citations, figures, and tables.
4. Synthesizer: novelty, gap analysis, cross-cutting insight, and contribution framing.
5. Newcomer: accessibility, missing definitions, and narrative flow.

## Scoring Protocol

- Score independently before aggregation.
- Use dimensions: novelty, empirical validation, clarity, technical depth, and significance.
- Treat early drafts as capped. A first pass should identify room to improve.
- Allow score increases only when concrete weaknesses are fixed in artifacts.
- Keep at least one unresolved weakness unless the final gate is genuinely ready.

## Weakness Routing

- Citation coverage or reference trust issues route to `paper-literature-survey`.
- Structure, taxonomy, claim strength, and transition issues route to `paper-structure-logic`.
- Missing experiments, weak baselines, or unclear statistics route to `paper-experiment-design`.
- Figure, table, caption, and result presentation issues route to `paper-figures-tables`.

## Final Gate

Before export, verify that the PDF compiles, claims are evidence-backed, citations are checked, figures and tables are referenced, reviewer regressions are absent, and no major weakness remains unresolved.
