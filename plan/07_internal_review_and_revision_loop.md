# Internal Review and Revision Loop

## Goal
Run internal review gates, route weaknesses, and trigger targeted revisions or reruns before PaperReview.ai.

## Inputs
- Reviewable manuscript and skill-check report.
- AI Scientist v1/v2 review outputs when available.
- DeepSeek peer-review simulation checklist.
- Claim/evidence and citation findings.

## Outputs
- Normalized internal review packets.
- Weakness routing report.
- Targeted revision or rerun tasks.
- Release-candidate readiness decision.

## Agent Owner
Agent 6: Review + Export.

## Instructions
- Normalize reviews into comparable strengths, weaknesses, scores, and action items.
- Use DeepSeek peer-review simulation as an internal gate.
- Route weaknesses to writing fixes, citation fixes, evidence fixes, ARC reruns, AI Scientist branch reruns, or export blockers.
- Allow PaperReview.ai submission only when the PDF compiles, PDF size is at most 10 MB, the first 15 pages contain the core contribution/method/experiments/limitations, citation gate passes, claim gate has no blocking unsupported claims, internal review score is at least 6.5/10, no blocking issues remain, and no more than two high-severity issues remain.
- Use ARC rerun for scientific-substance failures: missing baseline, bad experiment design, failed experiment, unsupported result claim, weak hypothesis, novelty problem, missing literature family, wrong dataset, or wrong metric.
- Use local manuscript revision for presentation failures: unclear abstract, bad section order, weak transitions, poor captions, citation formatting, hype, thin limitations, or redundant paragraphs.
- Use AI Scientist v1 when a known template can provide a stronger controlled experiment.
- Use AI Scientist v2 when weak novelty or uncertain direction requires branch exploration.
- Create a MetaClaw skill when a recurring failure can be expressed as a reusable rule.
- Do not advance to PaperReview.ai while critical evidence, citation, or build gaps remain.
- Keep reviewer disagreements visible for Agent 1 to arbitrate.

## Acceptance Criteria
- At least one internal review packet exists for the draft.
- Every weakness is routed, deferred with reason, or escalated.
- Critical blockers prevent external review.
- Release-candidate readiness explicitly satisfies the PaperReview.ai gate thresholds.

## Handoffs
- Hand evidence/citation fixes to Agent 5.
- Hand branch rerun requests to Agent 4.
- Hand ARC/mainline rerun requests to Agent 2.
- Hand release-candidate packet requirements to Agent 6's PaperReview.ai stage.
