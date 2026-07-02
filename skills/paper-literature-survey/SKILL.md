---
name: paper-literature-survey
description: Literature recall, citation scoring, citation depth assignment, venue upgrade, and reference verification guidance.
metadata:
  category: experiment
  trigger-keywords: "literature,citation,reference,bibtex,related work,venue,arxiv,openreview,dblp,verification,shortlist"
  applicable-stages: "3,4,5,6,16,17,19,23"
  priority: "1"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from Scientific Paper Writing Skill Group: https://victorchen96.github.io/auto_research/skill/paper-writing.html"
---

## Purpose

Use this skill when the paper needs stronger literature coverage, citation planning,
or reference verification. It adapts survey-style guidance to an empirical
NeurIPS paper: cite enough prior work to support claims, but do not inflate the
bibliography with irrelevant papers.

## Literature Workflow

1. Recall: expand each core concept into query variants covering method names, synonyms, benchmarks, and known failure modes.
2. Score: rank candidates by recency, relevance to the claim, venue quality, empirical usefulness, and citation reliability.
3. Classify depth:
   - A-level: central prior work discussed in a paragraph or more.
   - B-level: important comparison discussed in a few sentences.
   - C-level: supporting evidence cited briefly.
   - D-level: not cited.
4. Upgrade venues: when an arXiv entry is accepted, prefer the accepted venue metadata and BibTeX entry.
5. Verify: check title, first author, year, venue, DOI or URL, and whether the cited paper actually supports the manuscript claim.

## Empirical Paper Defaults

- Every important empirical claim needs a citation, experiment result, or explicit limitation.
- Prefer primary sources for method claims and benchmark papers for dataset or metric claims.
- Avoid long citation strings. Pick the strongest two or three references unless the manuscript is explicitly surveying an area.
- Survey targets such as very large citation counts or arXiv-only ratios are advisory, not mandatory, for this empirical pipeline.

## Output Expectations

- `references.bib` contains verified, non-placeholder entries.
- `citation_plan.jsonl` or equivalent notes identify each citation's role and depth.
- Related work distinguishes this paper structurally, not just by being newer.
- Citation verification has zero known hallucinated references before export.
