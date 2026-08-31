# Module 09 - Retrievers

> **MLCourse - Agentic AI - Retrievers**

> Stage in the capstone: RETRIEVE - feeds the context block of the capstone RAG prompt.

A retriever is a uniform interface with one contract: query in, relevant
`Document` objects out. That is deliberately ALL it promises. Under the hood it
might be a vector search (module 08), keyword BM25, a hybrid of both, an
ensemble, or a re-ranked pipeline - callers neither know nor care. This
abstraction is what lets the capstone's RAG chain be written once and survive
every future upgrade of the retrieval strategy behind it.

## What you will learn

1. Why "retriever" exists as its own interface, separate from vector stores.
2. How `vectorstore.as_retriever()` turns module 08's stores into Runnables.
3. The difference between plain similarity search and MMR - and where
   `lambda_mult` sits between them.
4. How `k` and `fetch_k` cooperate inside MMR.
5. How to pipe a retriever straight into LCEL chains - no LLM required.

## From vector store to retriever

```python
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("What did Alice drink?")   # -> list[Document]
```

`.invoke()` is the same Runnable protocol your chains already speak, so a
retriever composes everywhere a chain step can appear. The store answers "what
is in my index"; the retriever answers "what should I fetch for THIS question".

## similarity vs MMR: intuition

| Mode | Picks | Failure mode | Fix knob |
|---|---|---|---|
| `"similarity"` (default) | The k nearest chunks, full stop | Near-duplicate chunks flood all k slots (chunk overlap makes this common) | - |
| `"mmr"` | Iteratively picks chunks that are relevant AND different from what is already picked | Can drift slightly off-topic when diversity pressure is too strong | `lambda_mult` |

Maximal Marginal Relevance scores each candidate as a blend:

```
MMR = lambda_mult * relevance_to_query  -  (1 - lambda_mult) * similarity_to_already_picked
```

- `lambda_mult=1.0`: pure relevance - behaves like plain similarity.
- `lambda_mult=0.0`: maximum diversity - redundancy fully penalized.
- `lambda_mult=0.5` (default): the usual sweet spot.

## k vs fetch_k: the two-stage funnel

MMR needs room to be picky, so it works in two stages:

1. **`fetch_k`**: pull this many nearest candidates from the index (a cheap
   similarity pass). Think "the shortlist".
2. **`k`**: from that shortlist, select k final documents via the MMR trade-off.

Rule of thumb: `fetch_k` several times larger than `k` (`k=3, fetch_k=20` is a
great default). If `fetch_k == k`, MMR has zero freedom - you silently get plain
similarity behavior with extra compute.

## Retrievers are Runnables

Because `.invoke()` is the universal LangChain verb, retrievers pipe directly
into LCEL - including the parallel fan-out form the capstone uses:

```python
chain = (
    {"context": retriever | format_docs,     # branch 1: fetch + flatten
     "question": RunnablePassthrough()}      # branch 2: raw question through
    | prompt                                  # both results fill the template
)
```

The dict step runs both branches on every invoke; their outputs become the
prompt variables. Module 10 attaches a real model after the prompt; the
notebook here proves the plumbing by printing the rendered prompt instead -
fully offline, zero API keys.

## When and how

**Use a retriever when:**

- Any chain or agent needs context it should not hardcode.
- You want to swap search strategies later without touching chain code.
- You need MMR-style de-duplication over overlapping chunk grids.
- You want one uniform seam to add re-ranking, hybrid search, or filtering.

**How to work with one:**

1. Start from `vectordb.as_retriever(search_kwargs={"k": 3})`.
2. Switch to `search_type="mmr"` with `fetch_k` when duplicates appear.
3. Tune `lambda_mult` only if you can SEE the redundancy problem.
4. Pipe it into a prompt via the fan-out dict pattern shown above.
5. Print retrieved chunks while debugging - never trust invisible retrieval.

## Common pitfalls

- **Forgetting score scaling**: distances (Chroma/FAISS, lower-is-better) and
  similarities (cosine, higher-is-better) are opposites. A `score_threshold`
  meant to keep good hits will silently keep the WORST ones if your sign logic
  assumes similarities. Check which convention your store uses before thresholding.
- **Expecting the retriever to rank perfectly**: retrieval quality is bounded by
  chunking (module 06) and embedding choice (module 07). A retriever cannot fix
   garbage-in; eyeball retrieved chunks early and often.
- Setting `k` too high: ten mediocre chunks dilute the prompt, cost tokens, and
  often hurt answer quality more than missing one marginal chunk would.
- Confusing `fetch_k` with `k` in similarity mode: `fetch_k` only matters for
  MMR; passing it to a similarity retriever changes nothing.
- Forgetting that `as_retriever()` returns a LIVE VIEW of the store: documents
  added later are instantly visible; there is no snapshot to invalidate.

## Contents

| Notebook | What it does |
|---|---|
| [01_retrievers_deepdive.ipynb](01_retrievers_deepdive.ipynb) | `as_retriever` basics; MMR vs similarity on Alice's repetitive passages; `lambda_mult` sweep; retriever piped into an LCEL prompt printed offline (no LLM). |

## Summary

The retriever interface decouples WHAT your agent asks for from HOW it is
found: query in, Documents out, Runnable throughout. `similarity` mode is the
fast default; MMR adds diversity control via `fetch_k`, `k`, and `lambda_mult`;
and because retrievers compose with `|`, they slot directly into the capstone's
RAG chain as the context provider. Next module finally adds the G to RAG:
a real model answering from the context this stage feeds it.
