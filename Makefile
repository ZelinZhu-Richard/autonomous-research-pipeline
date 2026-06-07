.PHONY: check-env gateway metaclaw test-gateway test-metaclaw run-arc-test inspect-run git-safe

check-env:
	@test "$$CONDA_DEFAULT_ENV" = "arpipe" || (echo "Activate env first: conda activate arpipe" && exit 1)

gateway: check-env
	set -a; . ./.env; set +a; python -m uvicorn scripts.llm_gateway:app --host 127.0.0.1 --port 8088 --app-dir .

metaclaw: check-env
	metaclaw start --mode skills_only

test-gateway:
	curl http://127.0.0.1:8088/v1/chat/completions \
	  -H "Authorization: Bearer local-dev-key" \
	  -H "Content-Type: application/json" \
	  -d '{"model":"research-default","messages":[{"role":"user","content":"Say exactly: gateway works"}]}'

test-metaclaw:
	curl http://127.0.0.1:30000/v1/chat/completions \
	  -H "Authorization: Bearer local-dev-key" \
	  -H "Content-Type: application/json" \
	  -d '{"model":"research-default","messages":[{"role":"user","content":"Say exactly: metaclaw works"}]}'

run-arc-full: check-env
	cd external/AutoResearchClaw && researchclaw run \
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

git-safe:
	git status --short
	@echo "Make sure .env and runs/raw are NOT staged."

leaderboard: check-env
	python scripts/build_leaderboard.py