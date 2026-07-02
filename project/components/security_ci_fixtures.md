# Security, CI, and Fixtures Component

## Canonical Stage Links
- `../../plan/00_pipeline_and_agents.md`
- `../../plan/01_arc_metaclaw_spine.md`
- `../../plan/04_parallel_ai_scientist_branches.md`
- `../../plan/05_evidence_citation_verification.md`
- `../../plan/09_final_audited_package.md`

## Ownership
Own generated-code execution policy, test fixtures, CI matrix, and release gates.

## Responsibilities
- Define sandbox policy for generated code and branch experiments.
- Define fixture layout for adapters, validators, reviews, and export.
- Build the CI matrix around contract tests, importer tests, sandbox smoke tests, and optional GPU tests.
- Enforce release gates using deterministic fixtures.
- Disable generated-code execution when Docker or an equivalent sandbox is unavailable.
- Keep AI Scientist live execution disabled by default in v0.

## Interfaces
- Inputs: adapter expected artifacts, validator requirements, run manifest settings, generated-code constraints.
- Outputs: fixture requirements, CI jobs, sandbox policy, release gate checks, negative test cases.
- Consumers: every component that runs code, imports artifacts, or gates release.

## Parallelization Notes
- Fixture requirements should be defined early so adapter agents build to the same target.
- Docker or equivalent sandbox is required before generated-code execution.
- No NVIDIA GPU is assumed by default; GPU tests are optional future checks.
- CI can start with local/import tests and add GPU jobs later.

## Acceptance Criteria
- Happy-path and adversarial fixtures exist for each critical importer or validator.
- Generated code never runs directly on the host from bridge code.
- CI covers schemas, importers, citation/review validators, and export readiness.
- Optional GPU tests are clearly separated from required unit/import tests.
- Import-only AI Scientist fixtures are supported before any live branch execution.

## Open Questions
- Which Docker or equivalent sandbox command should CI use?
- What network egress is allowed for retrieval, package setup, experiment, review, and export stages?
