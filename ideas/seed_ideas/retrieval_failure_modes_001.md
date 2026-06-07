# Research Idea

Title: Diagnosing Retrieval Failure Modes with Parametric Synthetic Technical Documents

Topic:
Build a small CPU-compatible benchmark to analyze when sparse, dense, and hybrid retrieval fail on technical documents.

Core research question:
How do lexical overlap, semantic paraphrase, and technical term density affect the performance of sparse retrieval, dense retrieval, and hybrid retrieval?

Hypothesis:
Sparse retrieval should perform better when exact terminology overlap is high, dense retrieval should perform better under paraphrase, and hybrid retrieval should be more robust across mixed conditions.

Experiment design:
Generate a synthetic technical-document QA dataset where three factors are independently controlled:
1. lexical overlap between question and answer-support document
2. semantic paraphrase level
3. technical term density

Compare:
- keyword/BM25-style retrieval
- simple dense embedding retrieval
- hybrid retrieval

Metrics:
- Recall@k
- MRR
- failure rate by condition

Constraints:
- CPU-compatible only
- small synthetic dataset
- no broad claims
- include limitations
- produce a short LaTeX-style research draft
