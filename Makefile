.PHONY: check-env check-codex-cli gateway gateway-codex metaclaw test-gateway test-gateway-codex test-metaclaw run-arc-full extract-arc-test show-registry extract-run extract-claims show-claims inspect-run diagnose-stage5 git-safe leaderboard

check-env:
	@test "$$CONDA_DEFAULT_ENV" = "arpipe" || (echo "Activate env first: conda activate arpipe" && exit 1)

check-codex-cli:
	codex --version
	@echo "If this works but gateway-codex fails auth, run: codex login"

gateway: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; python -m uvicorn scripts.llm_gateway:app --host 127.0.0.1 --port 8088 --app-dir .

gateway-codex: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; CODEX_CLI_ENABLED=1 python -m uvicorn scripts.llm_gateway:app --host 127.0.0.1 --port 8088 --app-dir .

metaclaw: check-env
	metaclaw start --mode skills_only

test-gateway:
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; curl http://127.0.0.1:8088/v1/chat/completions \
	  -H "Authorization: Bearer $$GATEWAY_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model":"research-default","messages":[{"role":"user","content":"Say exactly: gateway works"}]}'

test-gateway-codex:
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; curl http://127.0.0.1:8088/v1/chat/completions \
	  -H "Authorization: Bearer $$GATEWAY_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model":"research-default","messages":[{"role":"user","content":"Say exactly: codex gateway works"}]}'

test-metaclaw:
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; curl http://127.0.0.1:30000/v1/chat/completions \
	  -H "Authorization: Bearer $$GATEWAY_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model":"research-default","messages":[{"role":"user","content":"Say exactly: metaclaw works"}]}'

run-arc-full: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; cd external/AutoResearchClaw && researchclaw run \
	  --config ../../configs/researchclaw.yaml \
	  --topic "$$(cat ../../ideas/seed_ideas/retrieval_failure_modes_001.md)" \
	  --output ../../runs/raw/arc_retrieval_full_001 \
	  --mode thorough \
	  --auto-approve \
	  --skip-noncritical-stage

extract-arc-test: check-env
	python scripts/extract_arc_run.py runs/raw/arc_retrieval_001 arc_retrieval_001

show-registry:
	tail -n 5 registries/idea_registry.jsonl | python -m json.tool

extract-run: check-env
	@test -n "$(RUN_DIR)" || (echo "Usage: make extract-run RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	@test -n "$(RUN_ID)" || (echo "Usage: make extract-run RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	python scripts/extract_arc_run.py $(RUN_DIR) $(RUN_ID)

extract-claims: check-env
	@test -n "$(RUN_DIR)" || (echo "Usage: make extract-claims RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	@test -n "$(RUN_ID)" || (echo "Usage: make extract-claims RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	python scripts/extract_claims.py $(RUN_DIR) $(RUN_ID)

show-claims:
	tail -n 20 registries/claim_registry.jsonl | python -m json.tool

inspect-run: check-env
	python scripts/inspect_run.py runs/raw/arc_retrieval_001

diagnose-stage5:
	@test -n "$(RUN_DIR)" || (echo "Usage: make diagnose-stage5 RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	@test -n "$(RUN_ID)" || (echo "Usage: make diagnose-stage5 RUN_DIR=runs/raw/arc_retrieval_001 RUN_ID=arc_retrieval_001" && exit 1)
	python scripts/diagnose_stage5.py $(RUN_DIR) $(RUN_ID)

git-safe:
	git status --short
	@echo "Make sure .env and runs/raw are NOT staged."

leaderboard: check-env
	python scripts/build_leaderboard.py
