# Module 11: Reranking

> **MLCourse - Agentic AI - Advanced RAG**

Add a second retrieval stage that *reads* each candidate against the query. A fast retriever finds 50 plausible documents; a cross-encoder then reorders them so the 3-5 chunks that actually reach the LLM are the best ones available.

## What the concept is

Ordinary vector search uses a **bi-encoder**: the query and each document are embedded *separately* and compared with a dot product. That is what makes it fast enough to scale to millions of documents - the document vectors are computed once, offline.

A **cross-encoder** does the opposite. It concatenates the query and one document into a single input and runs a transformer over the pair, so every query token can attend to every document token. Its relevance judgement is far better, and it cannot be precomputed - so it can only be afforded on a small candidate set.

The **retrieve-then-rerank** pattern uses each where it is strong:

```
query -> STAGE 1 retrieve (bi-encoder / BM25 / hybrid RRF, top 50)   -> goal: RECALL
      -> STAGE 2 rerank   (cross-encoder, keep top 5)                -> goal: PRECISION
      -> LLM generation
```

## Why it matters

- It is the **single most standard quality upgrade** in production RAG, and the cheapest one to add to a system you have already built.
- Reranking cost is **independent of corpus size** - it scales with the candidate count, which you choose.
- Rerank latency is usually a small slice of end-to-end latency, because the LLM generation call dominates.
- It is measurable. This module ends with a real precision@k and MRR delta on a fixed question set, not a claim.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_rerank](01_why_rerank.ipynb) | Bi-encoder recall vs cross-encoder precision; the two-stage pattern |
| 02 | [02_cross_encoder_reranking](02_cross_encoder_reranking.ipynb) | The `sentence-transformers` `CrossEncoder` API in practice |
| 03 | [03_rerank_over_hybrid](03_rerank_over_hybrid.ipynb) | Reranking the RRF output from `01_hybrid_search` |
| 04 | [04_measuring_the_lift](04_measuring_the_lift.ipynb) | Precision@k and MRR, before vs after, honestly reported |
| 05 | [05_latency_and_cost_tradeoff](05_latency_and_cost_tradeoff.ipynb) | What it costs, and when not to ship it |

### Walkthrough

**01 - Why rerank.** Embeds a question and shows that the *answer* passage often scores lower than a rephrasing of the question. Measures the cross-encoder's cost per pair and extrapolates: scoring a million documents is impossible, scoring 50 is trivial. Ends with the full two-stage pipeline and two Groq answers - one from the raw dense top-3, one from the reranked top-3.

**02 - Cross-encoder reranking.** The API up close. Raw logits and why they are neither probabilities nor comparable across queries; batching (measurably several times faster than per-pair calls, identical scores); a demonstration that input truncation is *silent* and collapses the score once the answer falls past 512 tokens; a model-choice table; and a reusable `CrossEncoderReranker` class that accepts candidates from any first stage.

**03 - Rerank over hybrid.** Rebuilds the module-01 retriever (BM25 + dense + RRF, `k=60`) and puts the cross-encoder behind it. Explains the key distinction: RRF is *positional* and never reads text, so it can only reward retriever agreement; the cross-encoder is the first component that reads. Tracks how far documents climb - paragraphs sitting at rank 20-25 routinely enter the final top 5, which is why the candidate set must be wide.

**04 - Measuring the lift.** Defines relevance with keyword rules written *before* the experiment, then evaluates four configurations (dense, bm25, hybrid, hybrid+rerank) at k = 1, 3, 5, 10 plus MRR. Reports the per-question win/tie/loss breakdown, not just the mean, and discusses honestly why a small clean corpus caps the achievable lift.

**Measured result on this corpus** (237 paragraphs, 8 questions):

| k | hybrid | hybrid+rerank | absolute | relative |
|---|---|---|---|---|
| 1 | 0.500 | 0.500 | +0.000 | +0.0% |
| 3 | 0.333 | 0.458 | **+0.125** | **+37.5%** |
| 5 | 0.275 | 0.325 | +0.050 | +18.2% |
| 10 | 0.200 | 0.250 | +0.050 | +25.0% |

MRR: 0.682 -> 0.698 (**+0.016, +2.3%**). Per question: 2 improved, 5 unchanged, 1 regressed.

**05 - Latency and cost.** Times every stage, plots rerank cost against candidate count to get a marginal ms-per-candidate figure, and converts a latency budget into a candidate budget. Compares the local cross-encoder against an LLM reranker on Groq (roughly two orders of magnitude slower, and it competes with generation for the same token budget). Ends with an explicit ship / do-not-ship checklist.

## How to run

```bash
# from the repository root
.venv/Scripts/python.exe -m jupyter lab
```

Open the notebooks in order and run all cells. They are self-contained - each loads `GROQ_API_KEY` from `03_agentic_ai/.env` by walking up the directory tree, so the working directory does not matter.

- **LLM**: Groq, `qwen/qwen3.8-27b`. The free tier is roughly 8000 tokens/minute; every loop paces itself and backs off exponentially.
- **Fallback**: a local Ollama server at `localhost:11434` - replace `ChatGroq` with `ChatOllama(model="llama3.1:8b")` and nothing else changes.
- **Models downloaded on first run**: `all-MiniLM-L6-v2` (bi-encoder, ~80 MB) and `cross-encoder/ms-marco-MiniLM-L-6-v2` (~80 MB), both cached afterwards.
- **Data**: `03_agentic_ai/data/alice.txt`.

## Prerequisites

- [01_hybrid_search](../01_hybrid_search/README.md) - BM25, dense retrieval and RRF; notebook 03 builds directly on it
- LangChain [08_vector_stores](../../01_langchain/08_vector_stores/README.md) and [09_retrievers](../../01_langchain/09_retrievers/README.md)
- LangChain [10_basic_rag](../../01_langchain/10_basic_rag/README.md)

## When to use this technique

- Your retriever returns the right document, but ranked 6th or 10th - a **precision** problem
- Your corpus is large or noisy enough that the top-5 contains real distractors
- You can afford to widen stage 1 to 30-100 candidates
- You have an LLM generation call whose latency the reranker can hide behind

Do **not** reach for it when the right document is not retrieved at all - that is a recall problem, and [12_query_transformation](../12_query_transformation/README.md) is the module for it.

## Next

[12_query_transformation](../12_query_transformation/README.md) - improve the query instead of the ranking.
