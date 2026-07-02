# Pipeline Questions and Decisions

## Run Defaults

### Question: Which target venue should ARC and PaperReview.ai optimize for?

Answer: ARC and PaperReview.ai should optimize for a NeurIPS-compatible format in v0.

Default:

```yaml
venue:
  target_venue: "neurips"
  display_name: "NeurIPS-compatible"
  arc_template_preference: "neurips"
  paperreview_target: "NeurIPS"
  domain_profile: "general_ml_agents"
  paper_type: "empirical"
```

Reason:

* AutoResearchClaw is most compatible with NeurIPS / ICML / ICLR-style ML paper workflows.
* NeurIPS is a strong default for agentic-research, ML systems, and empirical AI papers.
* AAAI and ICAIF should be added later as venue overlays, not built into v0.
* v0 should prove the bridge loop first, not fight custom formatting and venue-specific policy details.

Future venue profiles should be reserved here:

```text
bridge/venue_profiles/neurips.yaml   # v0
bridge/venue_profiles/aaai.yaml      # future
bridge/venue_profiles/icaif.yaml     # future
bridge/venue_profiles/icml.yaml      # future
bridge/venue_profiles/iclr.yaml      # future
```

---

### Question: Should the default paper type be empirical, survey, theory, demo, or mixed?

Answer: The default paper type should be empirical.

Default:

```yaml
paper:
  target_venue: "neurips"
  type: "empirical"
  mode: "paper_grade"
```

Allowed paper types:

```text
empirical
survey
theory
demo
mixed
```

Reason:

* ARC and AI Scientist are strongest when there is a concrete experiment, metric, baseline, and result.
* Empirical mode exercises the most important parts of the bridge: experiments, claims, citations, reviews, and quality gates.
* Survey mode should exist later, but it requires stricter literature-quality checks.

---

### Question: What seed idea should be the first full pipeline run?

Answer: The first full pipeline seed idea should be:

```text
Robust Citation and Review-Gate Feedback Loops for Autonomous Research Agents
```

Concrete research question:

```text
Can a bridge-level citation registry, claim registry, and review-issue router reduce unsupported claims, missing citations, and unresolved reviewer weaknesses in autonomous research-agent outputs?
```

Why this seed is correct:

* It tests the bridge itself.
* It does not require huge GPU compute.
* It can use existing ARC outputs and synthetic corrupted fixtures.
* It directly exercises citation validation, claim validation, review routing, MetaClaw skill creation, and PaperReview-style feedback.
* It creates a paper about the system being built.

v0 experiment:

```text
Take ARC-generated paper artifacts.
Inject controlled failures:
  - missing BibTeX key
  - duplicate citation key
  - unsupported claim
  - missing baseline comment
  - vague reviewer weakness
Run bridge validators and routers.
Measure detection rate, false positives, and repair routing accuracy.
```

---

## Upstream Sources

### Question: Which commits should be pinned for AutoResearchClaw, AI Scientist v1, AI Scientist v2, and MetaClaw?

Answer: Pin the exact commit that successfully passes the bridge import test for each upstream repo.

Do not pin floating `main`.

Required upstream repos:

```text
AutoResearchClaw
MetaClaw
AI-Scientist
AI-Scientist-v2
```

Create:

```text
external/LOCKFILE.md
external/LOCKFILE.json
```

Local command to collect SHAs:

```bash
git ls-remote https://github.com/aiming-lab/AutoResearchClaw.git HEAD
git ls-remote https://github.com/aiming-lab/MetaClaw.git HEAD
git ls-remote https://github.com/SakanaAI/AI-Scientist.git HEAD
git ls-remote https://github.com/SakanaAI/AI-Scientist-v2.git HEAD
```

Lockfile format:

```json
{
  "AutoResearchClaw": {
    "repo": "https://github.com/aiming-lab/AutoResearchClaw.git",
    "commit": "TODO_AFTER_LOCAL_PIN",
    "role": "primary_execution_spine"
  },
  "MetaClaw": {
    "repo": "https://github.com/aiming-lab/MetaClaw.git",
    "commit": "TODO_AFTER_LOCAL_PIN",
    "role": "cross_run_skill_memory"
  },
  "AI-Scientist": {
    "repo": "https://github.com/SakanaAI/AI-Scientist.git",
    "commit": "TODO_AFTER_LOCAL_PIN",
    "role": "template_based_experiment_branch"
  },
  "AI-Scientist-v2": {
    "repo": "https://github.com/SakanaAI/AI-Scientist-v2.git",
    "commit": "TODO_AFTER_LOCAL_PIN",
    "role": "open_ended_tree_search_branch"
  }
}
```

---

### Question: Should the external skill repositories be cloned into `external/`, referenced remotely, or converted into local MetaClaw skills only when needed?

Answer: Clone or pin upstream projects into `external/`, but treat skill guidance as local compiled policy.

Recommended layout:

```text
external/
  AutoResearchClaw/
  MetaClaw/
  AI-Scientist/
  AI-Scientist-v2/
  LOCKFILE.md
  LOCKFILE.json
```

Use git submodules or pinned clones. Do not copy upstream source code directly into the bridge unless intentionally patching it.

Canonical skill source:

```text
skills/
```

Compiled exports:

```text
.agents/skills/      # Codex skills
.claude/skills/      # ARC / Claude-compatible skills
~/.metaclaw/skills/  # optional live MetaClaw export
```

Rule:

```text
Repo-local skills are canonical.
User-level MetaClaw skills are generated exports.
```

---

### Question: Which skill repositories should be allowed to execute code, if any, instead of being used as policy/check sources?

Answer: In v0, no external skill repositories should execute code.

Allowed to execute code in v0:

```text
AutoResearchClaw adapter
bridge validators
bridge normalizers
local test fixtures
```

Not allowed to execute code in v0:

```text
random external skills
paper-writing skill page code
gpt_academic
paper-qa
A-Evolve
untrusted community skills
```

External skills should be treated as:

```text
policy/check sources
prompt guidance
validator checklists
MetaClaw/Codex/ARC skill material
```

---

### Question: Which skill repositories should be skipped entirely for the first working version?

Answer: Skip all nonessential external skill repositories in v0.

Skip:

```text
gpt_academic
paper-qa
A-Evolve
untrusted community skills
random external skill repos
```

Use only:

```text
AutoResearchClaw
MetaClaw
AI-Scientist
AI-Scientist-v2
DeepSeek-style paper-writing guidance as policy text
PaperReview.ai manual review import
```

v0 should not become a giant dependency jungle.

---

### Question: Should skill guidance be converted into MetaClaw `SKILL.md` files, bridge validator checklists, or both?

Answer: Both.

Convert skill guidance into:

```text
1. MetaClaw / ARC / Codex SKILL.md files
2. Bridge validator checklists
```

Rule:

```text
Skills guide behavior.
Validators decide pass/fail.
```

Do not rely on `SKILL.md` alone for correctness.

---

## Models and Credentials

### Question: Which provider/model should ARC use by default?

Answer: ARC should use the bridge alias `research_default`.

For hard stages, ARC should use `research_strong`.

Hard ARC stages:

```text
HYPOTHESIS_GEN
EXPERIMENT_DESIGN
CODE_GENERATION
RESULT_ANALYSIS
PAPER_DRAFT
PEER_REVIEW
QUALITY_GATE
CITATION_VERIFY
```

Cheap ARC stages:

```text
SEARCH_STRATEGY
LITERATURE_COLLECT
artifact normalization
formatting
simple classification
```

Model alias policy:

```yaml
models:
  research_strong: "${RESEARCH_STRONG_MODEL}"
  research_default: "${RESEARCH_DEFAULT_MODEL}"
  research_fast: "${RESEARCH_FAST_MODEL}"
  research_review: "${RESEARCH_REVIEW_MODEL}"
  research_code: "${RESEARCH_CODE_MODEL}"
  research_citation: "${RESEARCH_CITATION_MODEL}"
```

Do not hardcode provider names throughout the codebase.

---

### Question: Which provider/model should MetaClaw proxy traffic use?

Answer: MetaClaw should use:

```text
research_fast for skill injection and summarization
research_strong for lesson synthesis
```

Default MetaClaw mode:

```text
skills_only
```

Do not start with RL mode.

---

### Question: Which provider/models should AI Scientist v1 and v2 use for experiment, writeup, citation, review, and plotting steps?

Answer: Use bridge model aliases.

Mapping:

```text
research_code      → code generation
research_strong    → experiment planning and writeup
research_review    → internal review
research_citation  → citation checks
research_fast      → plotting, parsing, metadata, cleanup
```

Do not make AI Scientist v1/v2 hardcode vendor models. Route them through bridge config where possible.

---

### Question: Which environment variables should be required before live runs start?

Answer: Minimum required variables:

```bash
RESEARCH_GATEWAY_BASE_URL=
RESEARCH_GATEWAY_API_KEY=
RESEARCH_DEFAULT_MODEL=
RESEARCH_STRONG_MODEL=
RESEARCH_FAST_MODEL=
RESEARCH_CODE_MODEL=
RESEARCH_REVIEW_MODEL=
RESEARCH_CITATION_MODEL=
ARC_CONFIG_PATH=
BRIDGE_RUN_ROOT=
```

Optional variables:

```bash
OPENAI_API_KEY=
HACKCLUB_API_KEY=
HACKCLUB_BASE_URL=
SEMANTIC_SCHOLAR_API_KEY=
OPENALEX_EMAIL=
PAPERREVIEW_EMAIL=
TAVILY_API_KEY=
ANTHROPIC_API_KEY=
DEEPSEEK_API_KEY=
```

Do not require PaperReview credentials for v0 because v0 uses manual upload/import.

---

## Parallel Branch Scope

### Question: Should AI Scientist v1 and v2 both run on every serious pipeline run?

Answer: No.

Default:

```yaml
ai_scientist_v1:
  enabled: false
  mode: "on_template_fit"

ai_scientist_v2:
  enabled: false
  mode: "on_branch_need"
```

AI Scientist v1 should run only when:

```text
the topic matches an existing template
baseline run is available
the experiment can run locally or inside controlled container
```

AI Scientist v2 should run only when:

```text
ARC output has weak novelty
ARC has multiple plausible hypotheses
review says the experiment direction is weak
the bridge needs branch exploration
compute budget allows it
```

---

### Question: Should one branch be skipped when ARC output is already strong or compute is limited?

Answer: Yes.

Skip AI Scientist branches when:

```text
ARC quality gates pass
internal review has no high/blocking weaknesses
citation and claim gates pass
compute budget is low
Docker/GPU requirements are not met
```

AI Scientist branches are sidecars, not mandatory stages.

---

### Question: What is the maximum budget for branch runs?

Answer: v0 should use import-only AI Scientist branches.

Default v0:

```yaml
branch_budget:
  ai_scientist_v1_live_runs: 0
  ai_scientist_v2_live_runs: 0
  import_existing_runs_only: true
```

v1 after v0:

```yaml
branch_budget:
  ai_scientist_v1_live_runs: 1
  ai_scientist_v2_max_branches: 3
  max_wall_clock_hours: 2
  max_cost_usd: 10
  require_manual_approval: true
```

Serious later version:

```yaml
branch_budget:
  ai_scientist_v1_live_runs: 1
  ai_scientist_v2_max_branches: 5
  max_wall_clock_hours: 6
  max_cost_usd: 25
  require_manual_approval: true
```

---

## Evidence and Review Gates

### Question: Should paper-qa and gpt_academic be mandatory citation/literature checks or optional helper checks?

Answer: Optional helper checks only.

Reason:

* v0 already has enough moving parts.
* Mandatory citation truth should come from bridge citation registry, source registry, ARC verification report, and deterministic validators.
* External helpers can be added after the core validator layer works.

---

### Question: Should DeepSeek survey thresholds apply only in survey mode?

Answer: Survey-specific thresholds should apply only in survey or literature-heavy mode.

Apply globally:

```text
hallucinated citations = 0
claim strength <= evidence strength
major claims need evidence
experiment must support a named claim
```

Apply only in survey/literature-heavy mode:

```text
LQS threshold
A/B/C/D citation depth classification
arXiv-only ratio target
200-500 candidate recall target
within-1-year paper ratio
accepted-paper ratio
```

---

### Question: Which internal review score or weakness threshold blocks PaperReview.ai submission?

Answer: PaperReview.ai submission is allowed only if:

```text
paper PDF compiles
paper is <= 10MB
first 15 pages contain the core contribution, method, experiments, and limitations
citation gate passes
claim gate has no blocking unsupported claims
internal review score >= 6.5 / 10
no unresolved blocking issues
no more than 2 unresolved high-severity issues
```

If these fail, fix internally first. Do not waste external review on obviously broken output.

---

### Question: Which writing-skill checks are mandatory before internal review starts?

Answer: Required before internal review starts:

```text
citation integrity check
claim-evidence check
experiment-to-claim mapping
baseline coverage check
figure/table provenance check
abstract-conclusion alignment check
limitations section exists
related work coverage check
no unverified numeric result in paper
```

---

### Question: Which review findings require an ARC rerun versus a local manuscript revision?

Answer: Use ARC rerun when the problem is scientific substance.

ARC rerun:

```text
missing baseline
bad experiment design
failed experiment
unsupported result claim
weak hypothesis
novelty problem
missing literature family
wrong dataset or metric
```

Local manuscript revision:

```text
unclear abstract
bad section order
weak transitions
poor figure captions
citation formatting
too much hype
too little limitation discussion
redundant paragraphs
```

Use AI Scientist v1 when:

```text
the experiment fits a known template
a stronger controlled experiment is needed
```

Use AI Scientist v2 when:

```text
the problem is weak novelty or uncertain research direction
multiple hypotheses need exploration
```

Use MetaClaw skill creation when:

```text
the same type of failure is likely to recur
the fix can be expressed as a reusable rule
```

---

## PaperReview.ai

### Question: What email should be used for PaperReview.ai submission?

Answer: Do not hardcode email in source code.

Use:

```bash
PAPERREVIEW_EMAIL=
```

Default:

```text
Use your project/research email.
```

Store it in `.env.local`, not in committed files.

---

### Question: Should submission remain manual until a public API is documented?

Answer: Yes. v0 should use manual submission only.

PaperReview adapter v0 should support:

```text
generate review-ready PDF
generate first-15-pages PDF variant
record manual submission metadata
import pasted/downloaded review text
parse review into review_issue.json
```

Do not build a fake API adapter unless an official API exists.

---

### Question: Should the pipeline always generate a first-15-pages review variant PDF?

Answer: Yes.

Always generate:

```text
paperreview_first15.pdf
```

Reason:

* PaperReview.ai analyzes the first 15 pages.
* The bridge should make sure the first 15 pages contain the core contribution, method, experiment, results, limitations, and references if possible.

---

### Question: What target venue should be sent to PaperReview.ai when the final venue is undecided?

Answer: For v0, send:

```text
NeurIPS
```

Fallback for truly non-ML or unsupported future targets:

```text
Other
```

Do not leave the venue blank unless the topic is clearly outside supported venues.

---

## Runtime and Package

### Question: Is Docker or another rootless runtime available for generated-code execution?

Answer: Assume Docker or equivalent sandbox is required.

v0 rule:

```text
Generated-code execution requires Docker or equivalent sandbox.
```

If Docker is unavailable:

```text
disable generated-code execution
allow artifact import only
allow validator tests only
allow dry-run adapters only
```

Never run LLM-generated experiment code directly on the host in v0.

---

### Question: Is an NVIDIA GPU available for AI Scientist live runs?

Answer: Default assumption:

```text
No NVIDIA GPU available.
```

Therefore:

```text
AI Scientist v2 live execution disabled by default.
AI Scientist v1 live execution disabled unless template is CPU-feasible.
ARC sandbox may run small CPU experiments only.
```

If GPU exists:

```text
enable only after sandbox check passes
```

---

### Question: Where should final audited packages be written?

Answer: Write final packages to:

```text
runs/bridge/<bridge_run_id>/outputs/final_bundle/
```

Optionally create:

```text
dist/<bridge_run_id>.tar.gz
```

Final bundle should include:

```text
paper.pdf
paper.tex
report.md
report.html
references.bib
run_manifest.json
artifact_manifest.json
source_registry.json
citation_registry.json
claim_registry.json
experiment_registry.json
review_registry.json
quality_gate_report.json
branch_decision_log.jsonl
LOCKFILE.json
```

---

### Question: Should final packages copy large upstream artifacts or reference them by path and hash?

Answer: Reference large upstream artifacts by path plus SHA-256 hash by default.

Default:

```text
Reference large upstream artifacts by path + sha256 hash.
```

Do not copy every raw upstream artifact into the final bundle by default.

Use:

```bash
make package-full
```

only when a fully self-contained archive is needed.

---

## Agent Read Paths

### Question: Should every autonomous research agent read root `AGENTS.md` before any `plan/` or `project/` files?

Answer: Yes.

Every autonomous research/coding agent must read:

```text
AGENTS.md
```

first.

Root `AGENTS.md` should contain:

```text
project purpose
non-negotiable safety rules
build order
allowed write paths
required test commands
where to find project-specific instructions
```

---

### Question: Should `project/README.md` be the canonical multi-agent entry point after `AGENTS.md`?

Answer: Yes.

After `AGENTS.md`, agents should read:

```text
project/README.md
```

This is the canonical multi-agent project entrypoint.

---

### Question: Should agent-specific instructions live only in `project/agents/`, or should some be copied into root `AGENTS.md`?

Answer: Agent-specific instructions should live in:

```text
project/agents/
```

Examples:

```text
project/agents/codex.md
project/agents/metaclaw.md
project/agents/arc.md
project/agents/reviewer.md
```

Do not copy huge duplicated instructions into root `AGENTS.md`.

Root `AGENTS.md` should point to the specialized files.

---

### Question: Should generated MetaClaw skills live in repo-local `skills/`, user-level `~/.metaclaw/skills`, or both?

Answer: Both, but repo-local `skills/` is canonical.

Canonical source:

```text
skills/
```

Repo-local compiled exports:

```text
.agents/skills/
.claude/skills/
```

Optional user-level export:

```text
~/.metaclaw/skills/
```

Rule:

```text
Repo-local skills are canonical.
User-level MetaClaw skills are generated exports.
Never silently mutate ~/.metaclaw/skills during tests.
```

Use explicit command:

```bash
make export-metaclaw-skills
```
