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

run-arc-test: check-env
	cd external/AutoResearchClaw && researchclaw run \
	  --config ../../configs/researchclaw.yaml \
	  --topic "$$(cat ../../ideas/seed_ideas/retrieval_failure_modes_001.md)" \
	  --output ../../runs/raw/arc_retrieval_001 \
	  --mode express \
	  --auto-approve \
	  --to-stage EXPERIMENT_DESIGN

inspect-run: check-env
	python scripts/inspect_run.py runs/raw/arc_retrieval_001

git-safe:
	git status --short
	@echo "Make sure .env and runs/raw are NOT staged."
