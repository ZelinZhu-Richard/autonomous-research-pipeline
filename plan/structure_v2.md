
structure.md for the AutoResearchClaw MetaClaw AI Scientist Bridge
Executive summary
The cleanest architecture is not to make every upstream system a co-equal orchestrator. AutoResearchClaw already exposes a full 23-stage research pipeline with resumability, stage gating, detailed artifact trees, MetaClaw integration hooks, and a Python API. MetaClaw is best treated as the cross-run skill and memory plane. AI Scientist v1 is best treated as a template-based experimental sidecar with strong file conventions. AI Scientist v2 is best treated as an exploratory tree-search sidecar for open-ended ideas. The DeepSeek paper-writing skill page is best treated as a declarative policy pack that supplies quality gates, routing rules, and artifact expectations. PaperReview.ai is best treated as an external terminal reviewer, not as an inner-loop executor.

The bridge should therefore have one master run manifest, one normalized artifact index, one event stream, one citation registry, one normalized review packet format, and one normalized skill packet format. It should run AutoResearchClaw as the default backbone, fork optional AI Scientist v1 and v2 branches at defined checkpoints, render DeepSeek-style rules into bridge validators plus MetaClaw SKILL.md files, and import PaperReview.ai only on release-candidate PDFs. That is the most robust way to maximize leverage without creating a fragile “orchestrator of orchestrators.” This recommendation follows directly from the fact that ARC is already end-to-end, MetaClaw already acts as a proxy and skill injector, AI Scientist v1 requires a fixed template structure, AI Scientist v2 expects idea JSON plus BFTS config, and PaperReview.ai publicly documents a browser upload workflow rather than a programmable API.

The most important sequencing answer is this: citation registry extraction should happen after any bibliography-producing stage, then be re-extracted and frozen after the final verified bibliography exists. In ARC, that means a provisional extraction after Stage 22 references.bib, then a verified extraction after Stage 23 references_verified.bib. In the DeepSeek skill flow, it means extraction immediately after Literature Survey emits references.bib and citation_plan.jsonl. In AI Scientist v1, it means parsing the working LaTeX tree and any generated bibliography after writeup. In AI Scientist v2, it means extracting once citations are gathered for writeup and again once the final paper artifact exists. External review, especially PaperReview.ai, should consume the frozen registry rather than precede it.

One more thing you should not ignore: the ARC docs show visible version drift. The README changelog highlights v0.3.x, the Co-Pilot guide labels v0.4.0, and the integration guide says it was last updated for v0.5.0. The README also foregrounds a deliverables/ bundle, while the integration guide enumerates a stage-* tree plus pipeline_summary.json. The bridge must normalize both layouts rather than assuming one canonical tree.

topic + venue + profile

bridge_run_manifest.json

Compile DeepSeek skill packets

Sync MetaClaw skills

AutoResearchClaw primary run

Provisional citation registry extraction

AI Scientist v1 branch from synthesized template

AI Scientist v2 branch from workshop markdown and idea JSON

Normalized review packets

Weakness router

ARC citation verification or equivalent

Frozen citation registry

PaperReview.ai release-candidate review

final export bundle



Show code
The diagram above is the recommended flow because ARC already has explicit stages for paper drafting, review, quality gating, archive/export, and citation verification; MetaClaw already learns cross-run skills from failures; AI Scientist v1 and v2 each have their own independent run directories; and PaperReview.ai expects a PDF plus optional venue and returns review feedback on that final paper object.

Source grounded system map
AutoResearchClaw. AutoResearchClaw is an end-to-end research pipeline that turns one topic into a paper, produces literature artifacts, experiment code, charts, reviews, and bibliography outputs, and supports both CLI-driven runs and a Python API. The integration guide documents eight phases and twenty-three stages, with concrete artifacts such as goal.md, candidates.jsonl, exp_plan.yaml, experiment_final.py, paper_draft.md, paper.tex, references.bib, verification_report.json, and pipeline_summary.json; it also documents resumability and stage-level restart.

MetaClaw. MetaClaw is a transparent proxy in front of a personal agent or OpenAI-compatible client that injects skills, can evolve skills automatically, can optionally do RL fine-tuning, can schedule updates during idle windows, and can store long-term memory. The public README documents skills_only, rl, and auto modes, a local proxy on port 30000 by default, a skill library stored in ~/.metaclaw/skills, and a memory store in ~/.metaclaw/memory; it also documents that skills are individual SKILL.md files and that the proxy can be wired manually or through OpenClaw and related agent front ends.

AI Scientist v1. AI Scientist v1 is a template-based autonomous research system. It expects an experiment template directory with experiment.py, plot.py, prompt.json, seed_ideas.json, and latex/template.tex; it writes generated ideas to ideas.json, copies the template into a timestamped result folder under results/<experiment>/, writes notes.txt, log.txt, reviews, PDFs, and run outputs such as run_<n>/final_info.json, and can optionally improve the paper after review. It also exposes a reusable review function that emits structured JSON with fields such as Summary, Strengths, Weaknesses, Originality, Quality, Clarity, Significance, Questions, Limitations, Ethical Concerns, Soundness, Presentation, Contribution, Overall, Confidence, and Decision.

AI Scientist v2. AI Scientist v2 removes human-authored experiment templates, starts from a topic-description markdown file, generates idea JSON via perform_ideation_temp_free.py, and then runs a best-first tree-search pipeline via launch_scientist_bfts.py. Its public docs show the ideation input structure Title, Keywords, TL;DR, and Abstract, the idea output JSON fields Name, Title, Short Hypothesis, Related Work, Abstract, Experiments, and Risk Factors and Limitations, and a run directory experiments/<timestamp>_<idea_name>_attempt_<n> that contains idea.md, idea.json, logs/0-run/experiment_results, token_tracker.json, token_tracker_interactions.json, one or more PDFs, review_text.txt, and review_img_cap_ref.json.

DeepSeek scientific paper-writing skill. The public skill page describes a hierarchical paper-writing system, not a runnable software package. It decomposes writing into Literature Survey, Paper Structure and Logic, Experiment Design, Academic Figures and Tables, and Peer Review Simulation, with explicit artifact expectations such as references.bib, citation_plan.jsonl, sections/*.tex, results.json, experiment_summary.md, figures/*.pdf, and tables/*.tex. It also publishes concrete quality gates, routing logic, and score targets, which makes it extremely useful as a bridge-native validator and skill specification layer.

PaperReview.ai. PaperReview.ai is a browser-based upload-and-review system. The public pages document a submission form that takes a PDF, email address, and optional target venue, analyzes the first fifteen pages, and later returns an AI-generated review. The technical overview explains that it converts the uploaded PDF to Markdown, retrieves related work from arXiv using generated search queries and Tavily, summarizes related papers, and generates a review. For ICLR-targeted submissions it also computes seven dimension scores and maps them to a final score, and the site notes that it currently supports English-language papers and that reviews may contain errors.

System	Primary role in the bridge	Upstream-consumed inputs	Upstream-produced artifacts	Why it should sit where it does	Sources
AutoResearchClaw	Primary orchestrator	topic, config, optional MetaClaw bridge config	artifacts/rc-*/stage-*, paper.tex, references.bib, verification_report.json, pipeline_summary.json	It already owns the broadest lifecycle and has resumability plus stage semantics.
MetaClaw	Skill, memory, and optional proxy plane	OpenAI-compatible traffic, skill files, optional RL/PRM config	~/.metaclaw/config.yaml, ~/.metaclaw/skills/*/SKILL.md, ~/.metaclaw/memory	It should not own research stages. It should enrich them.
AI Scientist v1	Template-bound experiment and review sidecar	template folder plus model/API settings	results/<experiment>/<timestamp>_<idea>/..., PDFs, reviews, run outputs	Strong when you can synthesize a fixed template from ARC artifacts.
AI Scientist v2	Open-ended exploratory sidecar	workshop markdown, BFTS config, optional code seed	experiments/<timestamp>_<idea>_attempt_<n>/...	Useful for branching beyond ARC’s main line when the space is open-ended.
DeepSeek skill page	Policy and validator source	topic, taxonomy, findings, compiled PDF	references.bib, citation_plan.jsonl, results.json, sections/*.tex, figures/*.pdf, tables/*.tex	It is a rubric and workflow spec, not a runtime to shell out to.
PaperReview.ai	External release-candidate reviewer	final/review PDF, email, optional venue	review content, optional score dimensions for ICLR	Manual or semi-manual only until a public API is documented.

Adapter contracts and upstream artifacts
Adapter model. Every adapter should expose the same bridge-facing surface: probe(), run(), import_run(), validate_config(), list_expected_artifacts(), and normalize_review(). The bridge should never read upstream folders ad hoc. It should ask the adapter to emit normalized artifact_manifest entries plus stage_event records. That matters because ARC, AI Scientist v1, and AI Scientist v2 all use different output trees, while MetaClaw and PaperReview.ai are not stage-tree systems at all.

autoresearchclaw adapter. Read these upstream files first: README.md, docs/integration-guide.md, docs/HITL_GUIDE.md, config.researchclaw.example.yaml, and the documented integration paths researchclaw/metaclaw_bridge/, researchclaw/evolution.py, researchclaw/llm/client.py, and scripts/metaclaw_start.sh. Reproduce locally with pip install -e ., researchclaw setup, researchclaw init, then researchclaw run --config config.arc.yaml --topic "..." --auto-approve, or call execute_pipeline() from Python. Minimal input should be { "topic": "...", "config_path": "...", "mode": "auto_approve|co_pilot|express|gate_only", "from_stage": null, "resume": false }. Minimal normalized output should be { "source_system": "autoresearchclaw", "run_dir": "artifacts/rc-.../", "paper_artifact": ".../stage-22/paper.tex", "bib_artifact": ".../stage-22/references.bib", "verified_bib_artifact": ".../stage-23/references_verified.bib", "summary_artifact": ".../pipeline_summary.json" }. Required environment should be whatever llm.api_key_env points to, commonly OPENAI_API_KEY, plus any PRM key if you enable metaclaw_bridge.prm. Error modes should include config validation failure, stage failure with resumable status, missing artifact layout due to version drift, and MetaClaw proxy unavailability with direct LLM fallback.

A representative ARC artifact tree, directly documented upstream, looks like this and should be treated as the authoritative import target even if a convenience deliverables/ folder also exists in some versions.

text
Copy
artifacts/rc-20260310-143200-a1b2c3/
  stage-9/exp_plan.yaml
  stage-13/experiment_final.py
  stage-17/paper_draft.md
  stage-18/reviews.md
  stage-20/quality_report.json
  stage-22/paper.tex
  stage-22/references.bib
  stage-23/verification_report.json
  stage-23/references_verified.bib
  pipeline_summary.json
If the runtime layout deviates, discover it locally with:

bash
Copy
find artifacts/<run-id> -maxdepth 3 -type f | sort
researchclaw report --run-dir artifacts/<run-id>
metaclaw adapter. Read README.md, extensions/metaclaw-openclaw/README.md, and the built-in skill tree under memory_data/skills/; for OPD and RL-specific flows, also inspect the example and script paths explicitly referenced in the README. Reproduce locally with pip install -e ., metaclaw setup, metaclaw start --mode skills_only, and optionally cp -r memory_data/skills/* ~/.metaclaw/skills/. Minimal input should be { "mode": "skills_only|rl|auto", "proxy_port": 30000, "skills_dir": "~/.metaclaw/skills", "api_base": ".../v1", "model_id": "...", "api_key": "env-or-config" }. Minimal normalized output should be { "source_system": "metaclaw", "proxy_url": "http://127.0.0.1:30000/v1", "skills_index": ["~/.metaclaw/skills/arc-.../SKILL.md"], "memory_store": "~/.metaclaw/memory", "health": "ready|degraded|down" }. Required settings and env are provider-dependent, but the bridge must support the documented config keys for proxy.port, skills.dir, rl.*, opd.*, and memory.*. Error modes should include unhealthy proxy, missing or unreadable skill directory, invalid provider configuration, and RL backend not installed. If the proxy is down, the bridge should degrade to direct LLM calls and still render skill packets to disk.

A minimal MetaClaw integration snippet should look like this after normalization. It is bridge-generated, but it reflects the public config surface and file layout.

yaml
Copy
metaclaw:
  mode: skills_only
  proxy_url: http://127.0.0.1:30000/v1
  skills_dir: ~/.metaclaw/skills
  memory_store: ~/.metaclaw/memory
  sync_policy:
    write_bridge_skills: true
    preserve_non_bridge_skills: true
If the exact SKILL.md header format is unclear in your installed version, discover it locally rather than guessing:

bash
Copy
find ~/.metaclaw/skills -maxdepth 2 -name SKILL.md | head -n 5 | xargs sed -n '1,80p'
metaclaw status
ai_scientist_v1 adapter. Read README.md, launch_scientist.py, ai_scientist/generate_ideas.py, ai_scientist/perform_experiments.py, ai_scientist/perform_review.py, and at least one concrete template directory such as templates/nanoGPT_lite/ including prompt.json, seed_ideas.json, and latex/template.tex. Reproduce locally with the documented template setup and then python launch_scientist.py --model <model> --experiment nanoGPT_lite --num-ideas 1; if you want a minimal smoke test, use an already-prepared lightweight template. Minimal input should be { "experiment": "nanoGPT_lite", "model": "...", "num_ideas": 1, "writeup": "latex", "parallel": 0, "engine": "semanticscholar|openalex" }. Minimal normalized output should be { "source_system": "ai_scientist_v1", "results_dir": "results/nanoGPT_lite/<timestamp>_<idea>", "idea_name": "...", "notes_path": ".../notes.txt", "pdf_path": ".../<idea>.pdf", "review_path": ".../review.txt", "review_improved_path": ".../review_improved.txt", "log_path": ".../log.txt" }. Required env depends on the chosen model and scholar engine and can include OPENAI_API_KEY, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY, S2_API_KEY, OPENALEX_MAIL_ADDRESS, and for Bedrock/Vertex configurations the related cloud credentials. Error modes should include missing baseline run_0, missing LaTeX dependencies, unsupported template/output format, review JSON extraction failure, and missing PDF after writeup.

The v1 bridge opportunity is obvious: generate a synthetic template from ARC artifacts, because upstream explicitly says custom templates are just experiment.py, plot.py, prompt.json, seed_ideas.json, and latex/template.tex, provided filenames and output JSONs match the expected format. That is the clean way to connect ARC to AI Scientist v1 without rewriting v1 internals.

A small upstream snippet proves the template assumptions you need to meet.

json
Copy
{ "system": "You are an ambitious AI researcher...", "task_description": "You are given the following file to work with..." }
json
Copy
[
  {
    "Name": "adaptive_block_size",
    "Title": "Adaptive Block Size: Dynamic Context Window Adjustment for Efficient Training"
  }
]
If the exact shape of run_0/final_info.json is missing in your checkout, discover it locally instead of hardcoding:

bash
Copy
jq . templates/<template>/run_0/final_info.json
find results/<experiment> -maxdepth 2 -type f | sort
ai_scientist_v2 adapter. Read README.md, bfts_config.yaml, launch_scientist_bfts.py, ai_scientist/perform_ideation_temp_free.py, and the workshop example ai_scientist/ideas/i_cant_believe_its_not_better.md. Reproduce locally in two steps: first ideation, then experiment run. The documented commands are python ai_scientist/perform_ideation_temp_free.py --workshop-file ai_scientist/ideas/my_research_topic.md --model ... --max-num-generations 20 --num-reflections 5, then python launch_scientist_bfts.py --load_ideas ai_scientist/ideas/my_research_topic.json --model_writeup ... --model_citation ... --model_review ... --model_agg_plots ... --num_cite_rounds 20, with --load_code and --add_dataset_ref optional. Minimal ideation input should be { "workshop_file": "ai_scientist/ideas/my_topic.md", "model": "...", "max_num_generations": 20, "num_reflections": 5 }. Minimal run input should be { "load_ideas": "ai_scientist/ideas/my_topic.json", "idea_idx": 0, "attempt_id": 0, "model_writeup": "...", "model_writeup_small": "...", "model_citation": "...", "model_review": "...", "model_agg_plots": "...", "num_cite_rounds": 20 }. Minimal normalized output should be { "source_system": "ai_scientist_v2", "idea_dir": "experiments/<timestamp>_<idea>_attempt_<n>", "idea_md": ".../idea.md", "idea_json": ".../idea.json", "token_tracker": ".../token_tracker.json", "review_text": ".../review_text.txt", "review_fig_refs": ".../review_img_cap_ref.json", "pdf": ".../*.pdf", "tree_log_dir": ".../logs/0-run/" }. Required env can include OPENAI_API_KEY, GEMINI_API_KEY, S2_API_KEY, and AWS credentials when using Bedrock. Error modes should include missing idea JSON, absent same-name .py file when --load_code is set, missing hf_dataset_reference.py when dataset references are requested, no produced PDF, and writeup or review being skipped.

The v2 bridge opportunity is also clear: synthesize the workshop markdown from ARC’s topic, problem decomposition, synthesis, and hypothesis outputs, because v2’s ideation input is just a structured topic-description markdown file. That is far cleaner than trying to jam ARC stage artifacts directly into BFTS internals.

A representative v2 idea seed and run folder look like this upstream.

markdown
Copy
# Title: I Can't Believe It's Not Better
## Keywords
negative results, deep learning, failure modes
## TL;DR
...
## Abstract
...
text
Copy
experiments/2026-06-07_foo_attempt_0/
  idea.md
  idea.json
  logs/0-run/
  token_tracker.json
  token_tracker_interactions.json
  review_text.txt
  review_img_cap_ref.json
  <paper>.pdf
If the exact BFTS log structure differs, discover it locally:

bash
Copy
find experiments/<run-id> -maxdepth 4 | sort
sed -n '1,120p' bfts_config.yaml
paperreview adapter. Read the public upload page and tech overview page. There is no public repository and no documented public API or CLI on those pages, so the safe implementation is a manual-submit plus import-review adapter until official automation surfaces. Minimal input should be { "pdf_path": "...", "email": "...", "target_venue": "ICLR|NeurIPS|..." }. Minimal normalized output should be { "source_system": "paperreview_ai", "submission_mode": "manual", "review_status": "submitted|available|imported", "review_packet_path": ".../paperreview.review_packet.json", "raw_html_path": ".../paperreview.raw.html" }. Error modes should include oversized PDF, non-English content, missing returned review, and low-value review if key content falls after page fifteen. Because the public flow is email-notified and asynchronous, do not put this in the inner retry loop. Make it a release-candidate checkpoint.

You should also be ruthless about review-PDF preparation. PaperReview.ai states that only the first fifteen pages are analyzed, so the bridge should produce a review_variant.pdf whose first fifteen pages contain the abstract, strongest related-work framing, method summary, main results, limitations, and references that matter most for the external review. If you do not do this, you are voluntarily throwing away review signal.

deepseek_paperwriting adapter. Do not implement this as a process launcher. Implement it as a local compiler from the published skill spec into bridge policy files and MetaClaw skill packets. The page explicitly defines inputs and outputs for five sub-skills and publishes phase routing plus quality gates. Minimal input should therefore be { "topic": "...", "taxonomy_keywords": [...], "bib_path": "...", "experiment_findings": "...", "compiled_pdf": "..." }, while minimal normalized output should be { "source_system": "deepseek_skill_pack", "skill_packets": [...], "quality_profile": ".../deepseek_quality_profile.yaml", "routing_table": ".../deepseek_weakness_router.yaml" }. Error modes should be specification drift in the public page, missing mapping from a weakness to a route, and applying survey-specific thresholds to a non-survey paper without explicit opt-in.

A representative published output contract from the DeepSeek skill page is exactly the kind of thing the bridge should ingest as policy.

text
Copy
Literature Survey
IN: topic + taxonomy keywords
OUT: references.bib + citation_plan.jsonl

Experiment Design
IN: conjecture or gap
OUT: results.json + experiment_summary.md

Academic Figures & Tables
IN: results.json + section placeholders
OUT: figures/*.pdf + tables/*.tex
Bridge contracts and pipeline design
The bridge-native contracts should be the only stable interface Codex implements against. Upstream systems can drift. Your contracts cannot. The table below is the recommended shape. It is inferred from the upstream artifacts and failure semantics already documented by ARC, MetaClaw, AI Scientist v1, AI Scientist v2, the DeepSeek skill page, and PaperReview.ai.

Contract file	Purpose	Required fields	Produced by	Consumed by
bridge_run_manifest.schema.json	Single source of truth for a bridge run	bridge_run_id, topic, workspace_root, orchestrator, state, adapters, source_runs, created_at	bridge core	all adapters, validators
artifact_manifest.schema.json	Normalized artifact index across systems	bridge_run_id, artifacts[] with artifact_id, source_system, role, path, sha256, created_at	adapters	validators, exporters, citation registry
stage_event.schema.json	Event stream and state transitions	event_id, bridge_run_id, event_type, stage, from_state, to_state, severity, ts	bridge core + adapters	UI, retry logic, reports
citation_registry.schema.json	Unified bibliography and cite-key registry	registry_id, status, entries[], sources[], frozen_at	citation extractor	review and export stages
review_packet.schema.json	Review normalization across ARC, AI Scientist, PaperReview	review_id, source_system, target_artifact_id, dimensions, weaknesses, action_items, raw_ref	review adapters	weakness router, dashboards
skill_packet.schema.json	Bridge-native skill representation rendered to MetaClaw and validators	skill_id, title, trigger_conditions, applies_to_stages, guidance_md, evidence, version	DeepSeek compiler + lesson miner	MetaClaw sync, gate engine

A small but crucial design decision: keep citation_registry.status as provisional, verified, or frozen. This lets you extract early and often without lying to yourself about what is final. ARC explicitly distinguishes unverified references.bib from verified references_verified.bib; the DeepSeek skill spec explicitly distinguishes raw survey retrieval from later verification; and both AI Scientist branches do citation-related work during writeup rather than at topic-ingest time.

The recommended bridge entity relations are straightforward. Artifacts are indexed once, events point to artifacts, the citation registry reconciles bibliography and inline keys, review packets point back to the paper or draft artifact they judged, and skill packets are produced either from published skill policies or from run-derived lessons.

bridge_run_manifest

artifact_manifest

stage_events

citation_registry

review_packets

skill_packets

MetaClaw SKILL.md render

weakness_router



Show code
Recommended minimal schema examples
The following schema examples are recommended bridge contracts, not upstream file formats. They are implementation-oriented abstractions grounded in the upstream systems documented above.

bridge_run_manifest.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "bridge_run_manifest",
  "type": "object",
  "required": [
    "schema_version",
    "bridge_run_id",
    "topic",
    "workspace_root",
    "orchestrator",
    "state",
    "adapters",
    "source_runs",
    "created_at"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "bridge_run_id": { "type": "string" },
    "topic": { "type": "string" },
    "workspace_root": { "type": "string" },
    "orchestrator": { "type": "string", "enum": ["autoresearchclaw_primary"] },
    "state": { "type": "string" },
    "adapters": { "type": "array", "items": { "type": "string" } },
    "source_runs": { "type": "array", "items": { "type": "object" } },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
artifact_manifest.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "artifact_manifest",
  "type": "object",
  "required": ["schema_version", "bridge_run_id", "artifacts"],
  "properties": {
    "schema_version": { "type": "string" },
    "bridge_run_id": { "type": "string" },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "artifact_id",
          "source_system",
          "role",
          "path",
          "media_type",
          "sha256",
          "created_at"
        ],
        "properties": {
          "artifact_id": { "type": "string" },
          "source_system": { "type": "string" },
          "source_run_id": { "type": "string" },
          "role": { "type": "string" },
          "path": { "type": "string" },
          "media_type": { "type": "string" },
          "sha256": { "type": "string" },
          "created_at": { "type": "string", "format": "date-time" },
          "provenance": { "type": "object" }
        }
      }
    }
  }
}
stage_event.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "stage_event",
  "type": "object",
  "required": [
    "schema_version",
    "event_id",
    "bridge_run_id",
    "event_type",
    "stage",
    "from_state",
    "to_state",
    "severity",
    "ts"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "event_id": { "type": "string" },
    "bridge_run_id": { "type": "string" },
    "event_type": { "type": "string" },
    "stage": { "type": "string" },
    "from_state": { "type": "string" },
    "to_state": { "type": "string" },
    "severity": { "type": "string", "enum": ["info", "warning", "error"] },
    "message": { "type": "string" },
    "artifact_ids": { "type": "array", "items": { "type": "string" } },
    "ts": { "type": "string", "format": "date-time" }
  }
}
citation_registry.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "citation_registry",
  "type": "object",
  "required": [
    "schema_version",
    "registry_id",
    "bridge_run_id",
    "status",
    "sources",
    "entries"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "registry_id": { "type": "string" },
    "bridge_run_id": { "type": "string" },
    "status": { "type": "string", "enum": ["provisional", "verified", "frozen"] },
    "sources": { "type": "array", "items": { "type": "string" } },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["cite_key", "source_files", "verification_status"],
        "properties": {
          "cite_key": { "type": "string" },
          "aliases": { "type": "array", "items": { "type": "string" } },
          "title": { "type": "string" },
          "authors": { "type": "array", "items": { "type": "string" } },
          "year": { "type": "integer" },
          "venue": { "type": "string" },
          "doi": { "type": "string" },
          "arxiv_id": { "type": "string" },
          "inline_mentions": { "type": "array", "items": { "type": "string" } },
          "source_files": { "type": "array", "items": { "type": "string" } },
          "verification_status": { "type": "string" },
          "confidence": { "type": "number" }
        }
      }
    },
    "frozen_at": { "type": "string", "format": "date-time" }
  }
}
review_packet.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "review_packet",
  "type": "object",
  "required": [
    "schema_version",
    "review_id",
    "bridge_run_id",
    "source_system",
    "target_artifact_id",
    "raw_ref",
    "created_at"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "review_id": { "type": "string" },
    "bridge_run_id": { "type": "string" },
    "source_system": { "type": "string" },
    "target_artifact_id": { "type": "string" },
    "target_venue": { "type": "string" },
    "overall_score": { "type": ["number", "null"] },
    "decision": { "type": ["string", "null"] },
    "dimensions": { "type": "object" },
    "strengths": { "type": "array", "items": { "type": "string" } },
    "weaknesses": { "type": "array", "items": { "type": "string" } },
    "action_items": { "type": "array", "items": { "type": "string" } },
    "grounding_refs": { "type": "array", "items": { "type": "string" } },
    "raw_ref": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
skill_packet.schema.json

json
Copy
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "skill_packet",
  "type": "object",
  "required": [
    "schema_version",
    "skill_id",
    "title",
    "version",
    "trigger_conditions",
    "applies_to_stages",
    "guidance_md"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "skill_id": { "type": "string" },
    "title": { "type": "string" },
    "version": { "type": "string" },
    "source_system": { "type": "string" },
    "trigger_conditions": { "type": "array", "items": { "type": "string" } },
    "applies_to_stages": { "type": "array", "items": { "type": "string" } },
    "guidance_md": { "type": "string" },
    "evidence": { "type": "array", "items": { "type": "string" } },
    "severity_threshold": { "type": ["string", "null"] },
    "tags": { "type": "array", "items": { "type": "string" } }
  }
}
The bridge should also include these concrete adapter commands and Make targets. They are recommendations, but they mirror the upstream invocation surfaces closely enough to keep implementation friction low.

make
Copy
validate-contracts:
	python -m bridge.cli validate-contracts

arc-smoke:
	researchclaw run --config config.arc.yaml --topic "$(TOPIC)" --auto-approve

metaclaw-up:
	metaclaw start --mode skills_only --port 30000

aiv1-smoke:
	python launch_scientist.py --model "$(MODEL)" --experiment nanoGPT_lite --num-ideas 1

aiv2-ideate:
	python ai_scientist/perform_ideation_temp_free.py --workshop-file "$(IDEA_MD)" --model "$(MODEL)" --max-num-generations 3 --num-reflections 3

aiv2-run:
	python launch_scientist_bfts.py --load_ideas "$(IDEAS_JSON)" --idea_idx 0 --model_writeup "$(WRITEUP_MODEL)" --model_citation "$(CITATION_MODEL)" --model_review "$(REVIEW_MODEL)" --model_agg_plots "$(PLOT_MODEL)" --num_cite_rounds 8

import-paperreview:
	python -m bridge.cli import-paperreview --review-html "$(REVIEW_HTML)" --target-artifact "$(PDF_ARTIFACT_ID)"

e2e-bridge-smoke:
	python -m bridge.cli run --manifest bridge_run_manifest.json
Runtime policy, validators, and CI
The run lifecycle should be explicit, sparse, and resumable. ARC already has gate stages, resume support, and stage restarts; MetaClaw already degrades to direct calls when its proxy is unavailable; AI Scientist v1 and v2 both have multi-step runs where writeup and review can fail independently; PaperReview.ai is asynchronous and external. Your state machine should reflect that reality rather than pretending everything is synchronous and deterministic.

initialized

validated

running_primary

running_branch

waiting_gate

resumable_failure

review_pending

waiting_external_review

merging_feedback

citation_freeze

export_ready

completed

failed_terminal



Show code
The validator stack should be split into structural, evidentiary, citation, review, and security validators. Structural validators check presence, schema, hash, and provenance of expected artifacts. Evidentiary validators check that claims have metric-bearing experiment artifacts behind them. Citation validators reconcile .bib entries with inline cite keys and, where available, verified bibliographies. Review validators normalize scores and weakness lists across ARC, AI Scientist, DeepSeek-style review simulation, and PaperReview. Security validators check that generated code is executed only under the bridge sandbox rules. ARC’s own stage semantics and DeepSeek’s published quality gates are the right source material for these checks.

Use these gates as your “bulletproof enough to move on” standards:

Gate	Pass condition	Failure mode	Test fixture
Ingest gate	Required artifacts discovered and normalized	layout drift, missing run dir, bad hash	fixtures/arc/minimal_run
Citation gate	Registry extracted, keys reconciled, no unresolved duplicate cite keys, verified registry present if upstream provides one	broken .bib, inline key mismatch, hallucinated or unverified refs	fixtures/citations/arc_verified
Experiment evidence gate	Draft claims map to metric artifacts; for survey mode apply DeepSeek experiment gate only when experiments are expected	paper without supporting metrics, missing results.json, weak branch outputs	fixtures/aiv1/minimal_result, fixtures/aiv2/minimal_result
Review gate	At least one normalized review packet exists; weakness routing succeeds; no parse loss	malformed review JSON or HTML, unsupported score map	fixtures/reviews/aiv1, fixtures/reviews/paperreview
Release gate	citation registry frozen, export bundle complete, no unresolved critical validator findings	missing PDF, missing final bib, critical security incident	fixtures/export/release_candidate

For survey-mode runs, the DeepSeek page gives you usable concrete thresholds right now: citations at least 80 for a draft or at least pages×3 for a final paper, within-one-year references at least 40 percent, accepted papers at least 30 percent, arXiv-only references at most 60 percent, verification rate at least 80 percent, and every taxonomy cell covered by at least two A/B references. Do not apply these blindly to empirical short papers, but do support them as an optional quality_profile: deepseek_survey_v1.

Security is where most people get lazy and deserve the failure they get. Both AI Scientist versions explicitly warn that they execute LLM-written code and recommend controlled containerization, and ARC documents its own AST parsing, import whitelist, file-I/O restrictions, Docker execution mode, and network policy controls. The bridge should therefore enforce a stricter common denominator than any single upstream system: rootless containers, read-only base image, writable per-run workspace only, no host home mounts, default network=none during generated-code execution, explicit allowlist egress only during literature or package-setup stages, process-group kill on timeout, CPU and memory quotas, seccomp/AppArmor or equivalent, and artifact-only copy-out after completion. Generated code should never run directly on the host from bridge code.

A practical policy split is this. Retrieval stages may have narrow egress to documented literature sources or package mirrors when the selected upstream stage genuinely needs it. Generated experiment stages must run with no open web access. Review importers may parse local files only. PaperReview.ai submission should remain manual until a public API is documented. That policy is stricter than what upstream repos require, which is exactly why you should adopt it.

Your CI matrix should reflect documented platform requirements rather than wishful thinking. ARC’s docs say Python 3.11+; AI Scientist v2 targets Linux with NVIDIA GPUs using CUDA and PyTorch; AI Scientist v1 also assumes Linux and NVIDIA GPUs for the provided templates; MetaClaw’s plugin docs call for Python 3.11+ and note that heavy dependencies can stress low-RAM machines. So the sane matrix is: unit tests on Python 3.11 and 3.12 for contract logic; containerized integration tests on Ubuntu for artifact importers and validators; optional self-hosted GPU integration on CUDA 12.4 or equivalent for AI Scientist v2 and AI Scientist v1 smoke runs; and manual import tests for PaperReview.ai.

A recommended test matrix is below.

Job	Environment	What must pass
lint-unit	Ubuntu, Python 3.11 and 3.12	schemas, adapters, weakness router, citation extractor
fixtures-import	Ubuntu container	import ARC, v1, v2, MetaClaw skill dirs, sample review fixtures
sandbox-smoke	Ubuntu container with Docker-in-Docker or equivalent	rootless execution policy, timeout kill, network isolation
gpu-aiv1-smoke	self-hosted NVIDIA runner	one lightweight v1 run or fixture replay
gpu-aiv2-smoke	self-hosted NVIDIA runner	one ideation plus one minimal v2 run or fixture replay
manual-paperreview-canary	human-triggered	upload release-candidate PDF, import returned review, normalize into review_packet

Branch strategy and one week plan
Do not start with “full orchestration.” That is fake progress. Freeze the contracts first, then land adapters one by one, then add validators, then wire the end-to-end runner. If you skip that order, you will drown in path drift and parser hacks. The branch sequence below is the right one.

Branch	Scope	Bulletproof acceptance criteria
feat/contracts-core	All six bridge schemas, manifest loader, event model	JSON Schemas compile; golden examples validate; backward-compatibility tests for additive fields pass
feat/adapter-autoresearchclaw	ARC runner/importer/resume support	Can run or import one ARC run; discovers Stage 22 and Stage 23 bibliography artifacts; survives deliverables/ vs stage-* drift; emits artifacts and events cleanly
feat/adapter-metaclaw	MetaClaw probe, health, skill sync, skill render	Can start or probe proxy; can write bridge-generated SKILL.md; preserves existing skills; degrades cleanly when proxy is down
feat/adapter-ai-scientist-v1	v1 template synthesizer, runner, importer, review normalizer	Can build a minimal template, run one idea, import PDF plus review, and normalize v1 review JSON with no manual edits
feat/adapter-ai-scientist-v2	v2 ideation/run/import	Can generate workshop markdown, ideate to JSON, run one idea, import run dir, and extract review outputs if produced
feat/adapter-paperreview	Manual submit packet plus review importer	Produces upload-ready packet, release-candidate PDF, import script for returned review HTML or captured JSON, normalized review_packet
feat/validators-security	citation registry, gates, sandbox enforcement, fixture suite	All validators pass on happy-path fixtures and fail loudly on negative fixtures; sandbox rules enforced in CI
feat/orchestrator-e2e	full bridge CLI and branch routing	One end-to-end smoke path from topic to frozen citation registry and merged review queue passes

The “move on” rule is simple. A branch is done only when it has one happy-path fixture, one adversarial fixture, deterministic artifact imports, and a machine-readable acceptance test. If you cannot replay the fixture and get the same normalized manifests, the branch is not bulletproof. It is barely functional. That is not good enough for a bridge across six moving systems.

The first concrete next steps should be these:

text
Copy
Create bridge/contracts/
Create bridge/adapters/
Create bridge/validators/
Create fixtures/
Create docs/decision-log.md
Choose AutoResearchClaw as primary orchestrator
Pin upstream repos by commit in a lock file
Implement citation registry extraction immediately after bibliography-producing stages
The one-week implementation plan should look like this:

Day	Output
Monday	Freeze six bridge schemas, example instances, contract tests
Tuesday	Implement ARC adapter first, including import-only mode and citation-registry extraction from Stage 22 and Stage 23
Wednesday	Implement MetaClaw adapter plus skill_packet -> SKILL.md renderer; compile DeepSeek policy page into quality_profile and weakness_router
Thursday	Implement AI Scientist v1 adapter and template synthesizer from ARC artifacts; land review normalization for v1
Friday	Implement AI Scientist v2 ideation/run adapter; import idea.json, token tracking, PDFs, and reviews if present
Saturday	Implement PaperReview manual-submit/import path, release-candidate PDF generation, and review packet normalization
Sunday	Wire end-to-end runner, add validators, finalize fixtures, and run one full smoke path plus one negative path

The strongest possible v1/v2 bridge point is this. After ARC Stage 8 or Stage 9, synthesize either a v1 template or a v2 workshop markdown from ARC’s scoped problem, literature synthesis, and hypothesis outputs. After AI Scientist side branches complete, import their artifacts back as branch evidence, not as authoritative replacements for ARC. Use ARC to remain the canonical spine. Use MetaClaw to remember lessons across runs. Use DeepSeek to impose standards. Use PaperReview.ai only when you have a serious release candidate worth external scoring. That is the structure that is actually implementable and robust, not the fantasy of six masters fighting over the same run.