.PHONY: check-env check-codex-cli check-codex-beast gateway gateway-codex metaclaw test-gateway test-gateway-codex test-metaclaw test-codex-beast-shim show-topic run-arc-full run-arc-full-codex-beast extract-arc-test show-registry extract-run extract-claims show-claims inspect-run diagnose-stage5 git-safe leaderboard

ARC_RUN_DIR ?= runs/raw/arc_research_full_001
ARC_CODEX_BEAST_RUN_DIR ?= runs/raw/arc_research_full_codex_beast_001

check-env:
	@test "$$CONDA_DEFAULT_ENV" = "arpipe" || (echo "Activate env first: conda activate arpipe" && exit 1)

check-codex-cli:
	codex --version
	@echo "If this works but gateway-codex fails auth, run: codex login"

check-codex-beast:
	CODEX_BEAST_MODEL="$${CODEX_BEAST_MODEL:-gpt-5.5}" CODEX_CLI_REASONING_EFFORT="$${CODEX_CLI_REASONING_EFFORT:-xhigh}" PATH="$(CURDIR)/scripts:$$PATH" opencode --version
	codex --version

gateway: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; python -m uvicorn scripts.llm_gateway:app --host 127.0.0.1 --port 8088 --app-dir .

gateway-codex: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; CODEX_CLI_ENABLED=1 CODEX_CLI_MODEL="$${CODEX_CLI_MODEL:-gpt-5.5}" CODEX_CLI_REASONING_EFFORT="$${CODEX_CLI_REASONING_EFFORT:-xhigh}" python -m uvicorn scripts.llm_gateway:app --host 127.0.0.1 --port 8088 --app-dir .

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

test-codex-beast-shim:
	set -e; tmp_dir=$$(mktemp -d); trap 'rm -rf "$$tmp_dir"' EXIT; OPENCODE_CODEX_DRY_RUN=1 CODEX_BEAST_MODEL="$${CODEX_BEAST_MODEL:-gpt-5.5}" CODEX_CLI_REASONING_EFFORT="$${CODEX_CLI_REASONING_EFFORT:-xhigh}" PATH="$(CURDIR)/scripts:$$PATH" sh -c 'cd "$$1" && opencode run -m openai/research-default --format json "dry-run experiment generation"' sh "$$tmp_dir"; test -f "$$tmp_dir/main.py"

show-topic:
	@if [ -n "$(TOPIC_FILE)" ]; then echo "Topic source: TOPIC_FILE=$(TOPIC_FILE)"; cat "$(TOPIC_FILE)"; elif [ -n "$(TOPIC)" ]; then echo "Topic source: TOPIC"; printf '%s\n' "$(TOPIC)"; else echo "Topic source: configs/researchclaw.yaml research.topic"; PYTHONPATH=external/AutoResearchClaw python -c 'from researchclaw.config import RCConfig; print(RCConfig.load("configs/researchclaw.yaml", check_paths=False).research.topic)'; fi

run-arc-full: check-env
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; topic_value=""; topic_flag=""; if [ -n "$(TOPIC_FILE)" ]; then test -f "$(TOPIC_FILE)" || (echo "TOPIC_FILE not found: $(TOPIC_FILE)" && exit 1); topic_value="$$(cat "$(TOPIC_FILE)")"; topic_flag=1; elif [ -n "$(TOPIC)" ]; then topic_value="$(TOPIC)"; topic_flag=1; fi; cd external/AutoResearchClaw && if [ -n "$$topic_flag" ]; then python ../../scripts/run_researchclaw_hardened.py run \
	  --config ../../configs/researchclaw.yaml \
	  --topic "$$topic_value" \
	  --output ../../$(ARC_RUN_DIR) \
	  --mode full-auto \
	  --auto-approve \
	  --skip-noncritical-stage; else python ../../scripts/run_researchclaw_hardened.py run \
	  --config ../../configs/researchclaw.yaml \
	  --output ../../$(ARC_RUN_DIR) \
	  --mode full-auto \
	  --auto-approve \
	  --skip-noncritical-stage; fi

run-arc-full-codex-beast: check-env check-codex-beast
	set -a; . ./.env; set +a; : "$${GATEWAY_API_KEY:?Set GATEWAY_API_KEY in .env first}"; export CODEX_BEAST_MODEL="$${CODEX_BEAST_MODEL:-gpt-5.5}"; export CODEX_CLI_REASONING_EFFORT="$${CODEX_CLI_REASONING_EFFORT:-xhigh}"; python scripts/make_codex_beast_config.py configs/researchclaw.yaml runs/tmp/researchclaw.codex-beast.yaml; PATH="$(CURDIR)/scripts:$$PATH"; export PATH; topic_value=""; topic_flag=""; if [ -n "$(TOPIC_FILE)" ]; then test -f "$(TOPIC_FILE)" || (echo "TOPIC_FILE not found: $(TOPIC_FILE)" && exit 1); topic_value="$$(cat "$(TOPIC_FILE)")"; topic_flag=1; elif [ -n "$(TOPIC)" ]; then topic_value="$(TOPIC)"; topic_flag=1; fi; cd external/AutoResearchClaw && if [ -n "$$topic_flag" ]; then python ../../scripts/run_researchclaw_hardened.py run \
	  --config ../../runs/tmp/researchclaw.codex-beast.yaml \
	  --topic "$$topic_value" \
	  --output ../../$(ARC_CODEX_BEAST_RUN_DIR) \
	  --mode full-auto \
	  --auto-approve \
	  --skip-noncritical-stage; else python ../../scripts/run_researchclaw_hardened.py run \
	  --config ../../runs/tmp/researchclaw.codex-beast.yaml \
	  --output ../../$(ARC_CODEX_BEAST_RUN_DIR) \
	  --mode full-auto \
	  --auto-approve \
	  --skip-noncritical-stage; fi

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
