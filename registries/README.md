# Registries

These files are the truth layer of the autonomous research pipeline.

- idea_registry.jsonl: generated ideas, hypotheses, novelty scores, and source agent
- experiment_registry.jsonl: experiment commands, seeds, datasets, logs, and metrics
- claim_registry.jsonl: paper claims linked to evidence
- citation_registry.jsonl: citations and what claims they support
- review_registry.jsonl: external review feedback and fix status

Rule: no final paper claim should survive unless it is linked to either an experiment result or a verified citation.
