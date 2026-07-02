# Project State Audit

Generated: 2026-07-01

## Scope

This audit inspected the current local `autonomous-research-pipeline` workspace without changing behavior. It did not modify `external/AutoResearchClaw` or `external/MetaClaw`. `.env` was inspected only for variable names and set/missing status; no secret values were recorded.

## Commands Run

- `pwd`
- `git status --short`
- `find . -maxdepth 3 -type f`
- `make -n test-gateway`
- `python --version`
- `which python`

Additional read-only inspections covered `Makefile`, `scripts/`, `configs/`, `ideas/`, `registries/`, `reports/`, `runs/`, `external/`, `.gitignore`, and `~/.metaclaw/config.yaml` with API-key fields redacted.

## Environment

- Workspace: `/Users/richardzhu/dev/autonomous-research-pipeline`
- `CONDA_DEFAULT_ENV`: `base`
- `python --version`: `Python 3.13.9`
- `which python`: `/opt/anaconda3/bin/python`
- Risk: this shell is not currently in the expected `arpipe` environment. Several Makefile targets require `CONDA_DEFAULT_ENV=arpipe`.

## Git State

Current `git status --short` reported:

```text
 M .vscode/settings.json
 M Makefile
 M configs/researchclaw.yaml
 M scripts/llm_gateway.py
?? AGENTS.md
?? plan/
?? project/
```

Risk: there are existing modified/untracked files unrelated to this audit document. Do not commit or push without explicitly reviewing the full diff.

## Confirmed Existing Files

Top-level and project files:

- `.env`
- `.gitignore`
- `.vscode/settings.json`
- `AGENTS.md`
- `Makefile`
- `README.md`
- `configs/researchclaw.yaml`
- `docs/`

Scripts:

- `scripts/__init__.py`
- `scripts/build_leaderboard.py`
- `scripts/extract_arc_run.py`
- `scripts/extract_claims.py`
- `scripts/inspect_run.py`
- `scripts/llm_gateway.py`

Ideas:

- `ideas/seed_ideas/retrieval_failure_modes_001.md`
- `ideas/seed_ideas/test_001.md`

Registries and records:

- `registries/README.md`
- `registries/citation_registry.jsonl` with 0 lines
- `registries/claim_registry.jsonl` with 0 lines
- `registries/experiment_registry.jsonl` with 0 lines
- `registries/idea_registry.jsonl` with 2 lines
- `records/conversations.jsonl` with 6 lines
- `records/prm_scores.jsonl` with 0 lines

Reports:

- `reports/leaderboard.md`
- `reports/run_cards/arc_retrieval_001.md`
- `reports/review_cards/` exists as a directory

External repositories:

- `external/AutoResearchClaw`
- `external/MetaClaw`

Skills:

- `skills/` exists, but no files were found under it at max depth 3.

## Missing or Unknown Files

Expected or planned files not found in the current inspection:

- `scripts/doctor.py`
- `scripts/extract_citations.py`
- `scripts/recover_shortlist.py`
- `docs/local_workflow.md`
- `docs/debugging.md`
- `reports/debug/`
- `skills/paper_quality_gate.md`
- `skills/paper_writing_skill.md`

Unknown or not verified in this audit:

- Whether gateway and MetaClaw are currently running.
- Whether `researchclaw run --help` works in the current shell.
- Whether full ARC execution succeeds beyond the existing Stage 5 blocker.
- Exact `.env` values. Only variable names were inspected.

## Makefile Targets

Targets found in `Makefile`:

- `check-env`
- `check-codex-cli`
- `gateway`
- `gateway-codex`
- `metaclaw`
- `test-gateway`
- `test-gateway-codex`
- `test-metaclaw`
- `run-arc-full`
- `extract-arc-test`
- `show-registry`
- `extract-run`
- `extract-claims`
- `show-claims`
- `inspect-run`
- `git-safe`
- `leaderboard`

Dry-run check:

```text
make -n test-gateway
```

showed a `curl` call to `http://127.0.0.1:8088/v1/chat/completions` with model `research-default`.

Makefile consistency notes:

- `.PHONY` lists `run-arc-test`, but no `run-arc-test` rule body was found.
- `run-arc-full` exists as a rule but is not listed in `.PHONY`.
- Planned targets such as `doctor`, `run-arc-lit`, `run-arc-design`, `extract-citations`, and `process-run` are not present.

## Environment Variable Names in `.env`

The following variable names are present in `.env`; values were not printed:

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_MODEL`
- `GATEWAY_API_KEY`
- `HACKCLUB_API_KEY`
- `HACKCLUB_BASE_URL`
- `HACKCLUB_MODEL`
- `OPENAI_API_KEY`

Not observed in `.env`:

- `RESEARCH_GATEWAY_API_KEY`
- `RESEARCH_DEFAULT_MODEL`
- `RESEARCH_STRONG_MODEL`
- `RESEARCH_FAST_MODEL`
- `RESEARCH_CODE_MODEL`
- `RESEARCH_REVIEW_MODEL`
- `RESEARCH_CITATION_MODEL`

## Secret and Ignore Safety

`.gitignore` currently ignores:

- `.env`
- `*.log`
- `.DS_Store`
- `__pycache__/`
- `*.pyc`
- `runs/raw/`
- `runs/tmp/`
- `external/`
- common LaTeX temporary files
- `registries/*.jsonl`

`git check-ignore` confirmed these are ignored:

- `.env`
- `external/AutoResearchClaw`
- `runs/raw/arc_retrieval_001`
- `registries/idea_registry.jsonl`

## Current ARC Config LLM Routing

From `configs/researchclaw.yaml`, with secret fields redacted:

- `llm.provider`: `openai-compatible`
- `llm.base_url`: `http://127.0.0.1:8088/v1`
- `llm.wire_api`: `chat_completions`
- `llm.api_key_env`: `RESEARCH_GATEWAY_API_KEY`
- `llm.api_key`: present in config, redacted
- `llm.primary_model`: `research-default`
- `llm.fallback_models`: `[]`

Important routing note:

- ARC currently points directly to the local gateway on port `8088`.
- It does not currently point to MetaClaw on port `30000`.
- This differs from the earlier ARC -> MetaClaw -> gateway route described in prior planning notes.

Other relevant config state:

- `experiment.mode`: `sandbox`
- `experiment.sandbox.python_path`: `/opt/anaconda3/envs/arpipe/bin/python`
- `experiment.opencode.enabled`: `false`
- `experiment.figure_agent.enabled`: `false`
- `metaclaw_bridge.enabled`: `false`

## Current MetaClaw Config Routing

From `~/.metaclaw/config.yaml`, with secret fields redacted:

- `mode`: `skills_only`
- `llm.provider`: `custom`
- `llm.api_base`: `http://127.0.0.1:8088/v1`
- `llm.auth_method`: `api_key`
- `llm.model_id`: `research-default`
- `proxy.host`: `0.0.0.0`
- `proxy.port`: `30000`
- `rl.enabled`: `false`
- `skills.enabled`: `true`
- `skills.dir`: `/Users/richardzhu/dev/autonomous-research-pipeline/skills`
- `skills.auto_evolve`: `false`

Routing implication:

- MetaClaw is configured to listen on port `30000` and call the local gateway on port `8088`.
- Current ARC config bypasses MetaClaw unless changed back to `http://127.0.0.1:30000/v1`.

## Existing Run Folders

Raw run folders:

- `runs/raw/arc_retrieval_001`
- `runs/raw/arc_test_001`

Both runs include:

- `checkpoint.json`
- `config.yaml`
- `heartbeat.json`
- `pipeline_summary.json`
- `deliverables/manifest.json`
- `deliverables/neurips_2025.sty`
- `evolution/lessons.jsonl`
- `hitl/session.json`
- `stage-01/`
- `stage-02/`
- `stage-03/`
- `stage-04/`
- `stage-05/`
- `stage-06/`

`arc_retrieval_001` includes:

- `stage-01/goal.md`
- `stage-02/problem_tree.md`
- `stage-03/search_plan.yaml`
- `stage-03/queries.json`
- `stage-03/sources.json`
- `stage-04/candidates.jsonl`
- `stage-04/references.bib`
- `stage-04/search_meta.json`
- `stage-04/web_search_result.json`
- `stage-05/screen_meta.json`
- `stage-06/decision.json`

`arc_test_001` includes the same general stages and also has `stage-04/web_context.md`.

## Existing Run Status

`runs/raw/arc_retrieval_001/pipeline_summary.json` reports:

- `stages_executed`: 6
- `stages_done`: 4
- `stages_blocked`: 1
- `stages_failed`: 1
- `final_status`: `failed`

`runs/raw/arc_retrieval_001/stage-05/stage_health.json` reports:

- `status`: `blocked_approval`
- `error`: `Model returned empty shortlist after strict screening`

`runs/raw/arc_retrieval_001/stage-06/decision.json` reports:

- `status`: `failed`
- `error`: `Missing input: shortlist.jsonl (required by KNOWLEDGE_EXTRACT)`

`runs/raw/arc_test_001/pipeline_summary.json` reports the same high-level status:

- 6 stages executed
- 4 done
- 1 blocked
- 1 failed
- final status `failed`

`runs/raw/arc_test_001/stage-05/stage_health.json` also reports:

- `error`: `Model returned empty shortlist after strict screening`

## Current Reports

`reports/leaderboard.md` exists and lists two rows, both for `arc_retrieval_001`.

Risk: the leaderboard appears to contain a duplicate run ID row.

`reports/run_cards/arc_retrieval_001.md` exists.

No claim card files were found.

## Immediate Risks

1. Current shell is in `base`, not `arpipe`; Makefile `check-env` will fail until `conda activate arpipe` is used.
2. ARC config currently routes directly to gateway `8088`, bypassing MetaClaw `30000`.
3. `.env` has `GATEWAY_API_KEY`, but not `RESEARCH_GATEWAY_API_KEY`; current gateway code falls back to `GATEWAY_API_KEY`, but ARC config names `RESEARCH_GATEWAY_API_KEY`.
4. Existing raw runs are failed at Stage 5 because strict literature screening returned an empty shortlist.
5. Stage 6 fails because `shortlist.jsonl` is missing.
6. `reports/leaderboard.md` has duplicate `arc_retrieval_001` entries.
7. `scripts/doctor.py`, citation extraction, debug reports, and process-run automation are not present.
8. The repo has pre-existing modified and untracked files; staging/committing/pushing would be risky without reviewing those diffs.
9. `skills/` is empty, while MetaClaw config points to it as the enabled skills directory.
10. Gateway and MetaClaw runtime health were not checked in this audit; only config and dry-run targets were inspected.

## Recommended Next Step

Do not push yet. First review the existing dirty worktree, especially:

- `.vscode/settings.json`
- `Makefile`
- `configs/researchclaw.yaml`
- `scripts/llm_gateway.py`
- untracked `AGENTS.md`
- untracked `plan/`
- untracked `project/`

After deciding which changes are intended, commit only the selected files. This audit itself is safe to stage separately as `docs/project_state_audit.md`.
