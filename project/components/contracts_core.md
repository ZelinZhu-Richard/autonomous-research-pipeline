# Contracts Core Component

## Canonical Stage Links
- `../../plan/00_pipeline_and_agents.md`
- `../../plan/03_artifact_registry.md`
- `../../plan/09_final_audited_package.md`

## Ownership
Own the bridge-native contracts that all adapters, validators, and exporters consume.

## Responsibilities
- Define the run manifest, artifact manifest, stage event, citation registry, review packet, and skill packet contracts.
- Keep contract fields stable and additive where possible.
- Provide example instances for happy-path and failure-path fixtures.
- Ensure adapter components never read upstream folders ad hoc when normalized contracts should be used.

## Interfaces
- Inputs: topic/profile defaults, adapter selections, source-run references, upstream artifact paths.
- Outputs: schema files, example documents, validation results, and contract-level test fixtures.
- Consumers: ARC, MetaClaw, AI Scientist, citation, review, export, security, and CI components.

## Parallelization Notes
- Start this component before adapter implementation.
- Publish any schema field changes in `../coordination/decisions.md`.
- Coordinate with every component when adding required fields.

## Acceptance Criteria
- All six schemas compile.
- Golden examples validate.
- Additive-field compatibility tests pass.
- Every other component can state which contract files it reads or writes.

## Open Questions
- Where should schema files live in implementation: `bridge/contracts/`, `schemas/`, or another package path?
- Which manifest fields are required for MVP versus later live-run orchestration?
