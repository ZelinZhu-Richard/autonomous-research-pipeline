# AutoResearchClaw Primary Component

## Canonical Stage Links
- `../../plan/01_arc_metaclaw_spine.md`
- `../../plan/03_artifact_registry.md`
- `../../plan/05_evidence_citation_verification.md`

## Ownership
Own the AutoResearchClaw adapter as the canonical pipeline spine.

## Responsibilities
- Support ARC import, run, and resume flows.
- Normalize ARC artifacts into artifact manifest entries and stage events.
- Handle documented layout drift between `stage-*` outputs and convenience `deliverables/` bundles.
- Surface Stage 22 and Stage 23 bibliography artifacts for citation components.

## Interfaces
- Inputs: bridge run manifest, ARC config, topic/profile, optional existing run directory.
- Outputs: normalized artifact entries, stage events, ARC summary references, paper artifacts, and bibliography paths.
- Consumers: citation registry, review normalization, final export, and validator components.

## Parallelization Notes
- Can start after contracts define artifact and event shapes.
- Import-only mode can be built before live ARC runs.
- Coordinate with citations before changing bibliography role names.

## Acceptance Criteria
- Imports one minimal ARC run fixture deterministically.
- Finds draft and verified bibliography artifacts when present.
- Emits resumable failure state for interrupted ARC runs.
- Does not assume one canonical ARC artifact layout.

## Open Questions
- Which ARC commit should be pinned for adapter acceptance tests?
- Should MVP include live ARC execution or import-only support first?
