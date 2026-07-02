# Final Audited Package

## Goal
Assemble the final audited research package after ARC, sidecar branches, skill checks, evidence/citation verification, internal review, and PaperReview.ai gate are complete.

## Inputs
- Final manuscript and PDF.
- ARC run artifacts and MetaClaw learned skills.
- AI Scientist branch summaries and evidence.
- Frozen citation registry and claim/evidence audit.
- Internal and external review packets.
- Final decisions, waivers, and handoff notes.

## Outputs
- Final paper package.
- Audit summary with source systems and verification gates.
- Registry snapshots.
- Review and weakness-resolution summary.
- MetaClaw lesson/skill summary.
- Optional `dist/<bridge_run_id>.tar.gz` archive when a self-contained package is explicitly requested.

## Agent Owner
Agent 1: Lead/Integrator, supported by Agent 6: Review + Export.

## Instructions
- Include ARC mainline artifacts and clearly label sidecar evidence.
- Include final paper, references, figures/tables, registries, reviews, and decision logs.
- Write final packages to `runs/bridge/<bridge_run_id>/outputs/final_bundle/`.
- Include `paper.pdf`, `paper.tex`, `report.md`, `report.html`, `references.bib`, `run_manifest.json`, `artifact_manifest.json`, `source_registry.json`, `citation_registry.json`, `claim_registry.json`, `experiment_registry.json`, `review_registry.json`, `quality_gate_report.json`, `branch_decision_log.jsonl`, and `LOCKFILE.json` when available.
- Preserve raw review/import artifacts when useful, but make normalized packets the primary audit interface.
- Reference large upstream artifacts by path plus SHA-256 hash by default.
- Use `make package-full` only when a fully self-contained archive is needed.
- Record any unresolved weaknesses or waived gates.
- Make the package inspectable without guessing upstream run directories.

## Acceptance Criteria
- Final package contains paper artifacts, registries, review packets, audit summary, and source-system provenance.
- Frozen citations and evidence checks are included.
- PaperReview.ai status is included as passed, waived, unavailable, or unresolved.
- MetaClaw learned skills or lessons are listed for future runs.
- Large upstream artifacts are referenced by path and hash unless a full package was explicitly requested.

## Handoffs
- Agent 6 hands the release bundle to Agent 1.
- Agent 1 records final status, unresolved risks, and next-run lessons.
- Agent 1 updates coordination files and any final leaderboard/run-card records.
