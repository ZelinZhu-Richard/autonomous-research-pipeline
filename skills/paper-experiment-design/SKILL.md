---
name: paper-experiment-design
description: Hypothesis-linked empirical design, execution, iteration, statistics, and result reporting for paper claims.
metadata:
  category: experiment
  trigger-keywords: "experiment,hypothesis,baseline,ablation,statistics,results,trial,seed,confidence,benchmark,evaluation"
  applicable-stages: "8,9,12,13,14,15,17,19,20"
  priority: "1"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from Scientific Paper Writing Skill Group: https://victorchen96.github.io/auto_research/skill/paper-writing.html"
---

## Purpose

Use this skill when a paper claim needs empirical support. Each experiment must
answer which manuscript claim it supports or falsifies.

## Design Requirements

1. State the hypothesis before running or importing results.
2. Define independent variables, dependent variables, controls, datasets, metrics, and expected direction.
3. Choose baselines before seeing results.
4. Decide statistical reporting before execution to avoid post-hoc hypothesis changes.
5. Keep the first experiment minimal, but include enough controls to be interpretable.

## Execution Requirements

- Use at least three trials or seeds when stochasticity matters.
- Report mean and standard deviation or confidence intervals for repeated trials.
- Include ablations that isolate the mechanism being claimed.
- Record failure cases, ceiling effects, floor effects, and unexpected findings.
- If results are not significant, increase trials, revise task difficulty, or weaken the claim.

## Reporting Contract

- `results.json` should include config, conditions, raw or aggregate results, statistics, and findings.
- `experiment_summary.md` should state purpose, methods, main results, limitations, and supported manuscript claims.
- Do not generate polished LaTeX tables in this skill. Pass structured result material to the figures/tables skill.

## Reviewer Check

An experiment is not paper-ready unless a skeptical reviewer can identify the
claim, reproduce the setup, understand the baseline, and see uncertainty.
