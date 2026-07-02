# Stage 5 Diagnostic: arc_retrieval_001

## Run

- Run directory: `/Users/richardzhu/dev/autonomous-research-pipeline/runs/raw/arc_retrieval_001`
- Candidates: 627 rows in `stage-04/candidates.jsonl`
- References: `stage-04/references.bib`
- Shortlist: Missing
- Shortlist rows: 0

## Stage 5 Status

- Health file: `stage-05/stage_health.json`
- Decision file: `stage-05/decision.json`
- Status: blocked_approval
- Decision: block
- Error: Model returned empty shortlist after strict screening
- Duration seconds: 38.39
- Timestamp: 2026-06-07T03:49:54+00:00

## Stage 5 Metadata

```json
{
  "outcome": "model_rejected_all",
  "candidates_screened": 577,
  "shortlist_size": 0,
  "note": "Strict screen returned empty shortlist. Pipeline paused; consider rerunning SEARCH_STRATEGY with refined queries before resuming."
}
```

## Stage 6 Status

- Decision file: `stage-06/decision.json`
- Status: failed
- Decision: retry
- Error: Missing input: shortlist.jsonl (required by KNOWLEDGE_EXTRACT)

## Search Metadata

```json
{
  "real_search": true,
  "queries_used": [
    "# Research Idea\n\nTitle",
    "Diagnosing Retrieval Failure Modes with Parametric",
    "Build a small CPU-compatible benchmark to",
    "hybrid retrieval fail on technical documents.",
    "research idea",
    "idea diagnosing",
    "diagnosing retrieval",
    "retrieval failure"
  ],
  "year_min": 2020,
  "total_candidates": 627,
  "bibtex_entries": 621,
  "ts": "2026-06-07T03:49:16+00:00"
}
```

## Sample Candidates

| # | Title | Year | Venue | Source | Citations | DOI | URL |
|---:|---|---:|---|---|---:|---|---|
| 1 | Clinical course and risk factors for mortality of adult inpatients with COVID-19 in Wuhan, China: a retrospective cohort study | 2020 | The Lancet | openalex | 29105 | 10.1016/s0140-6736(20)30566-3 | https://doi.org/10.1016/s0140-6736(20)30566-3 |
| 2 | PRISMA 2020 explanation and elaboration: updated guidance and exemplars for reporting systematic reviews | 2021 | BMJ | openalex | 10811 | 10.1136/bmj.n160 | https://doi.org/10.1136/bmj.n160 |
| 3 | ColabFold: making protein folding accessible to all | 2022 | Nature Methods | openalex | 9576 | 10.1038/s41592-022-01488-1 | https://doi.org/10.1038/s41592-022-01488-1 |
| 4 | Review of deep learning: concepts, CNN architectures, challenges, applications, future directions | 2021 | Journal Of Big Data | openalex | 7484 | 10.1186/s40537-021-00444-8 | https://doi.org/10.1186/s40537-021-00444-8 |
| 5 | The PRIDE database resources in 2022: a hub for mass spectrometry-based proteomics evidences | 2021 | Nucleic Acids Research | openalex | 6706 | 10.1093/nar/gkab1038 | https://doi.org/10.1093/nar/gkab1038 |
| 6 | The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation | 2020 | BMC Genomics | openalex | 5758 | 10.1186/s12864-019-6413-7 | https://doi.org/10.1186/s12864-019-6413-7 |
| 7 | Advances and Open Problems in Federated Learning | 2020 | Foundations and Trends® in Machine Learning | openalex | 4663 | 10.1561/2200000083 | https://doi.org/10.1561/2200000083 |
| 8 | African Journal of Business Management | 2026 | AFRICAN JOURNAL OF BUSINESS MANAGEMENT | openalex | 4223 | 10.5897/ajbm | https://doi.org/10.5897/ajbm |
| 9 | Physical distancing, face masks, and eye protection to prevent person-to-person transmission of SARS-CoV-2 and COVID-19: a systematic review and meta-analysis | 2020 | The Lancet | openalex | 4078 | 10.1016/s0140-6736(20)31142-9 | https://doi.org/10.1016/s0140-6736(20)31142-9 |
| 10 | CP2K: An electronic structure and molecular dynamics software package - Quickstep: Efficient and accurate electronic structure calculations | 2020 | The Journal of Chemical Physics | openalex | 4058 | 10.1063/5.0007045 | https://doi.org/10.1063/5.0007045 |

## Diagnosis

- Stage 5 empty-shortlist blocker detected: True
- Stage 6 missing-shortlist failure detected: True
- Stage 6 appears downstream of Stage 5: knowledge extraction requires `shortlist.jsonl`, but Stage 5 produced no shortlist.
- No raw run artifacts were modified by this diagnostic.

## Recommended Next Actions

1. Inspect the sample candidates and Stage 4 search metadata for topic drift before rerunning.
2. Tune or rerun Stage 5 screening with less brittle criteria or improved retrieval queries.
3. Keep `shortlist.jsonl` recovery as an explicit operator-approved action; do not fabricate it during diagnostics.
4. Re-extract the run and rebuild the leaderboard after a repaired rerun produces a real shortlist.
