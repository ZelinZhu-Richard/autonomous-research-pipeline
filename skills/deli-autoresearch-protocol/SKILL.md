---
name: deli-autoresearch-protocol
description: Long-horizon autonomous research protocol for anti-loop state, stall detection, fresh-session iteration, and watchdog-style resilience.
metadata:
  category: tooling
  trigger-keywords: "long horizon,autonomous,stall,loop,watchdog,heartbeat,state,orchestrator,subagent,unattended,fragility,pivot"
  applicable-stages: "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23"
  priority: "1"
  version: "1.0"
  author: autonomous-research-pipeline
  references: "Synthesized from user-provided Deli_AutoResearch protocol attachment"
---

## Purpose

Use this skill when the research run may span many stages, long compute jobs, or
multiple autonomous iterations. It prevents three recurring failures: cognitive
loops, silent stalls, and fragile runtime supervision.

## Operating Principles

1. Persist progress to files, not conversation memory.
2. Treat preparation as leading to execution; do not stop after setup if the next action is routine.
3. Use fresh context for each major iteration and inject only curated state.
4. Separate work from evaluation. The worker produces artifacts; the orchestrator judges progress.
5. Prefer structural pivots over tactical parameter tuning after repeated stalls.
6. External dependency failures should produce a concrete report and retry path, not silent abandonment.

## State Files

For long-running subtasks, maintain a small state bundle:

- `state/task_spec.md`: goal, milestones, success criteria, and constraints.
- `state/progress.json`: iteration, status, stale count, and key metrics.
- `state/findings.jsonl`: append-only evidence or findings.
- `state/directions_tried.json`: strategies already attempted.
- `state/iteration_log.jsonl`: per-iteration summaries and decisions.

Use JSONL log events with timestamp, source, level, event, and detail. Mark
important choices with `level=decision`.

## Stall Detection

- If an iteration adds no useful finding or worsens the target metric, increment `stale_count`.
- At `stale_count >= 2`, force a new direction that changes a structural constraint.
- At `stale_count >= 4`, stop local nudging and surface a human-readable blocked report.
- Cap individual work sessions by round count or elapsed time; validate artifacts between iterations.

## Direction Diversity

Before launching a new iteration:

1. Read `directions_tried.json`.
2. Propose a direction that differs materially from prior attempts.
3. Record why the new direction changes the search space.
4. After a stall, perturb the frame: dataset, baseline, claim scope, evaluation axis, or retrieval strategy.

## Guardian Pattern

A guardian or watchdog may only check liveness, restart, or nudge. It must not
rewrite task artifacts or make scientific judgments for the worker. Its job is
to keep the loop alive and detect when work has become structurally stuck.

## Subagent Patterns

- Research iteration: inject tried directions and require verifiable findings.
- Parallel exploration: split into investigation, refutation, and cross-domain analogy.
- Experiment run: start polling immediately after submission; diagnose, fix, and resubmit routine failures.
- Verification: use an independent pass to audit evidence, citations, and artifact consistency.

## Paper Pipeline Adaptation

For this repo, apply the protocol to ARC runs by using stage artifacts as the
state source, not chat memory. Stage 04 retrieval failures, Stage 05 empty
shortlists, experiment retries, and manuscript review loops should all write
diagnostic artifacts that make the next run or resume decision mechanical.
