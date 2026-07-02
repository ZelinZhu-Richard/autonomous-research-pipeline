# Manuscript Build and Skill Checks

## Goal
Build the manuscript from ARC outputs and apply writing, structure, figure/table, and robustness checks from the skill policy stack.

## Inputs
- ARC paper draft, LaTeX, figures, tables, and bibliography.
- Branch evidence and result summaries.
- Skill policy checklist from Agent 3.
- Verified evidence and citation findings from Agent 5.

## Outputs
- Reviewable manuscript draft.
- PDF build artifact when available.
- Skill-check report covering writing quality, structure, citations, figures/tables, limitations, and result grounding.
- Revision queue for internal review.

## Agent Owner
Agent 6: Review + Export, supported by Agent 3: Skill Policy.

## Instructions
- Use ARC's paper output as the base manuscript.
- Apply skill policies as checks and revision guidance rather than competing manuscript generators.
- Require these checks before internal review starts: citation integrity, claim-evidence mapping, experiment-to-claim mapping, baseline coverage, figure/table provenance, abstract-conclusion alignment, limitations section, related-work coverage, and no unverified numeric result in the paper.
- Confirm major claims have evidence before polishing language.
- Validate figures/tables against reported results.
- Keep build errors, missing assets, and citation failures separate in the report.

## Acceptance Criteria
- A reviewable draft or explicit build failure report exists.
- Skill checks cover DeepSeek paper-writing categories and selected external writing skills.
- Figures, tables, references, and claims are checked against registered artifacts.
- Mandatory writing-skill checks pass before internal review starts, or the report states the blocker.
- Internal review can start from the built draft and skill-check report.

## Handoffs
- Receive policy checks from Agent 3 and verified evidence/citations from Agent 5.
- Hand draft, PDF, build report, and skill-check report to Agent 6 review loop.
- Hand unresolved build blockers to Agent 1.
