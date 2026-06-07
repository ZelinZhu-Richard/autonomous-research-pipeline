Pipeline:

idea seed
  ↓
AutoResearchClaw + MetaClaw run
  ↓
AI Scientist-v2 parallel run
  ↓
claim/result/citation registry
  ↓
paper-writing skill quality gates
  ↓
compile PDF
  ↓
PaperReview.ai review
  ↓
targeted rerun/fix
  ↓
final audited paper package


autonomous-research-pipeline/
  README.md
  docker-compose.yml
  Makefile
  .env.example
  .gitignore

  configs/
    researchclaw.yaml
    metaclaw.yaml
    ai_scientist.yaml
    review.yaml

  skills/
    paper_writing_skill.md

  ideas/
    seed_ideas/
    selected/

  runs/
    raw/
    processed/
    archived/

  registries/
    idea_registry.jsonl
    experiment_registry.jsonl
    claim_registry.jsonl
    citation_registry.jsonl
    review_registry.jsonl

  scripts/
    run_researchclaw.py
    run_ai_scientist.py
    merge_candidates.py
    verify_claims.py
    verify_citations.py
    score_paper.py
    compile_latex.py
    package_final.py

  papers/
    drafts/
    final/

  reports/
    run_cards/
    review_cards/
    leaderboard.md