# Module 15: Late Interaction Retrieval

> **MLCourse - Agentic AI - Advanced RAG**

Keep one embedding **per token** instead of one per passage, and compare query
tokens against document tokens at search time with an operator called
**MaxSim**. This is the ColBERT family, and it is the third option between the
bi-encoder you already use and the cross-encoder from module 11.

## What the concept is

Ordinary vector search is a **bi-encoder**: a whole passage is squashed into a
single vector ahead of time, the query is squashed into a single vector, and
the two are compared with one dot product. Fast, and lossy — averaging the
token vectors throws away *which* word matched *which*.

A **cross-encoder** (module 11) glues the query and one document together and
runs a transformer over the pair, so every query token attends to every
document token. Far more accurate, and impossible to precompute: there is
nothing to store until the query arrives.

**Late interaction** takes the useful half of each. The document is encoded
once, offline, into one vector per token — precomputable, exactly like a
bi-encoder. The interaction then happens at query time, but as cheap
arithmetic rather than a transformer:

$$\text{MaxSim}(Q, D) = \sum_{i} \max_{j} \; q_i \cdot d_j$$

For each **query** token, take its best match anywhere in the document
(`max`), then add those bests up across the query (`sum`). The name is
literal: the interaction is *late* (after encoding), as opposed to a
cross-encoder's *early* interaction.

```
query -> STAGE 1 retrieve (bi-encoder / hybrid / LATE INTERACTION, top ~100) -> RECALL
      -> STAGE 2 rerank   (cross-encoder, keep top ~5)                       -> PRECISION
      -> LLM generation
```

**Late interaction competes for stage 1.** It is a better *retriever*, not a
better reranker — see [`11_reranking`](../11_reranking/README.md) for stage 2,
which this module cross-links to rather than repeats.

## Where it sits

| | Bi-encoder | **Late interaction** | Cross-encoder |
|---|---|---|---|
| Covered in | `01_hybrid_search` | **this module** | [`11_reranking`](../11_reranking/README.md) |
| Doc representation | 1 vector | **1 vector per token** | none — reprocessed each time |
| Interaction | none (dot product) | **at query time, over stored vectors** | inside the transformer |
| Precomputable? | ✅ | **✅** | ❌ |
| Storage / passage | ~1.5 KB | **~40-70 KB uncompressed** | 0 |
| Role | first-stage retrieval | **first-stage retrieval** | reranking a shortlist |

## Why it matters

- It attacks **first-stage recall** — the one failure a reranker can never
  repair, because a passage missing from the shortlist cannot be reordered
  into it.
- Its scores **decompose per query token**, so a bad result can be debugged
  ("this query word found nothing") rather than shrugged at. Single-vector
  search offers no such handle.
- It is the clearest worked example of a general principle: *expensive scoring
  functions do not get cheaper, they get applied to fewer candidates.*
- The cost is **storage**, and this module measures it rather than asserting
  it.

## An honest note on what is implemented here

Installing `pylate` into this course's environment **downgrades `torch`,
`transformers` and `sentence-transformers`**, breaking other modules in this
track. It was tried and rolled back.

So this module is a **teaching reimplementation**: token embeddings come from
an ordinary `sentence-transformers` bi-encoder, and MaxSim is applied to them
by hand in NumPy.

- ✅ The **scoring mechanism** is the real one. MaxSim is MaxSim.
- ✅ The **storage and latency arithmetic** is the real one.
- ❌ The **quality numbers are not**. A real ColBERT is *trained* for this
  operator; we are borrowing token vectors from a model trained for pooled
  ones.

Every measurement in these notebooks states which category it falls into. For
real work, use `pylate`, `colbert-ai`, or `RAGatouille` in a clean environment.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_late_interaction](01_why_late_interaction.ipynb) | What a pooled vector throws away; the three families side by side |
| 02 | [02_token_embeddings_and_maxsim](02_token_embeddings_and_maxsim.ipynb) | Token embeddings, normalisation, MaxSim from scratch, the padding-mask bug |
| 03 | [03_late_interaction_retrieval](03_late_interaction_retrieval.ipynb) | A labelled benchmark: Recall@k and MRR, dense vs MaxSim, measured |
| 04 | [04_storage_and_latency_cost](04_storage_and_latency_cost.ipynb) | The bill: index size, dimension reduction, quantization, latency |

### Walkthrough

**01 — Why late interaction.** Runs ordinary vector search on a small corpus
and reports honestly that it *wins* — the bi-encoder ranks the answer first.
The interesting part is ranks 2 and 3, where a passage merely *about France*
and one using "capital" figuratively crowd the top. Introduces the three
families and ends with a token-alignment table (`capital → capital`,
`france → france`) that single-vector search structurally cannot produce.

**02 — Token embeddings and MaxSim.** Builds the operator properly. Measures
that token vector norms vary ~3× (so normalisation is not optional), explains
why the `max` is over documents and the `sum` over queries, and what breaks if
you swap them. Then the padding bug: **measured on this corpus, masking
changed nothing** — MiniLM's embedding space is anisotropic enough that a
zero padding row never wins a `max`. A synthetic 3-D example shows the case
where it *does* flip the ranking, and the rule stands: always mask before the
max.

**03 — Retrieval, measured.** A 24-passage corpus, 10 questions, one correct
answer each. **Result: dense and MaxSim tied on all ten questions** (MRR 0.950
each). The benchmark is saturated — Recall@3 is already 1.00 — so it had no
power to separate them, and the notebook says so rather than dressing it up. It
then measures something more useful: **filler tokens (`[CLS]`, `the`, `is`,
`what`) contribute ~68% of every MaxSim score**. Restricting the sum to content
tokens takes MRR to 1.000, moving the single question both other retrievers got
wrong — one question's worth of evidence, reported as such.

**04 — What it costs.** Measured: a token index is **46× larger** than a
single-vector one for these passages (the ratio is just the token count). At
a million passages that is 1.5 GB versus 70 GB. Shows the two compression
tricks — PCA down to 128/64 dims, scalar quantization to 8/4/2 bits — and
reaches roughly ColBERTv2's operating point at **1% of the uncompressed
size**. States plainly that the question set is too small to detect
compression's real quality cost. Measures MaxSim latency at 240-380× a dense
scan, explains why that ratio does not go away with better engineering, and
closes with a decision checklist that puts late interaction **last**, after
chunking, hybrid search, query rewriting, and reranking.

## Prerequisites

- [`01_hybrid_search`](../01_hybrid_search/README.md) — what a bi-encoder
  index is and how dense retrieval scores documents.
- [`11_reranking`](../11_reranking/README.md) — the bi-encoder vs
  cross-encoder distinction. This module assumes it and builds on it.
- [`10_rag_evaluation`](../10_rag_evaluation/README.md) — Recall@k and MRR,
  and why a saturated benchmark tells you nothing.

## Providers and keys

**None.** Every notebook in this module runs on a local embedding model
(`all-MiniLM-L6-v2`, ~80 MB, cached after first download) plus NumPy and
scikit-learn. There are **no LLM calls and no API key** anywhere in module 15.

## Setup

```powershell
pip install sentence-transformers scikit-learn
```

Nothing else. In particular, **do not `pip install pylate` into this course's
shared environment** — it downgrades `torch`, `transformers` and
`sentence-transformers` and breaks other modules.

## Key takeaways

- A pooled vector averages away **which token matched which** — the most
  useful signal for judging relevance.
- **MaxSim**: max over document tokens, then sum over query tokens. The
  asymmetry means "found anywhere in the passage" and "every query term
  counted separately".
- Always **mask padding before the max**, even though whether it bites depends
  on a property of your embedding space you probably have not checked.
- Late interaction is a **first-stage retriever**. It composes with
  cross-encoder reranking; it does not replace it.
- The cost is **storage** — roughly the token count, before compression.
- **Small benchmarks cannot settle retrieval questions.** Three of the four
  measurements in this module came back saturated, and saying so is part of
  the lesson.
