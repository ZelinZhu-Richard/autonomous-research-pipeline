---
name: paper-figures-tables
description: High-density academic tables, vector figures, captions, and result presentation rules.
metadata:
  category: writing
  trigger-keywords: "figure,table,caption,plot,chart,visualization,booktabs,error bars,results,ablation,benchmark"
  applicable-stages: "14,16,17,19,20"
  priority: "2"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from Scientific Paper Writing Skill Group: https://victorchen96.github.io/auto_research/skill/paper-writing.html"
---

## Purpose

Use this skill to turn evidence into inspectable tables and figures. Figures and
tables must carry scientific content, not decoration.

## Table Rules

- Use booktabs-style tables: no vertical rules, compact spacing, and clear grouping.
- Include deltas, baselines, or grouped conditions when they improve comparison.
- Bold only meaningful best values, and avoid hiding uncertainty.
- Experimental values should include mean plus standard deviation or confidence interval when repeated trials exist.
- Captions should state the takeaway, not only describe the table.

## Figure Rules

- Prefer vector PDF for plots and diagrams when practical.
- Use PNG only when raster output is necessary, and keep it at 300 DPI or better.
- Label all axes, include units, and provide legends for multi-line plots.
- Use light grids and readable font sizes after scaling.
- Every figure must be referenced in the text before or near where it appears.

## Artifact Expectations

- `figures/*.pdf` or high-resolution PNG for visual artifacts.
- `tables/*.tex` for manuscript tables when LaTeX output is available.
- Each visual maps to a paper claim, experiment result, taxonomy, or important comparison.

## Failure Modes

- A table is not ready if rows are incomparable or metrics are mixed without explanation.
- A figure is not ready if the reader needs the main text to understand the basic message.
- A caption is not ready if it lacks the conclusion the reader should draw.
