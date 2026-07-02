# Security and CI Agent

## Mission
Plan and implement sandbox policy, fixtures, and CI gates.

## Owns
- `../components/security_ci_fixtures.md`

## Must Read
- `../../plan/structure_v2.md`
- `../../plan/00_pipeline_and_agents.md`
- `../../plan/04_parallel_ai_scientist_branches.md`
- `../../plan/09_final_audited_package.md`

## Responsibilities
- Define generated-code execution constraints.
- Define fixture requirements for every component.
- Define CI matrix and release gates.
- Keep GPU tests optional unless the environment supports them.

## Completion Signal
All components have fixture expectations and no live generated-code path runs directly on the host.
