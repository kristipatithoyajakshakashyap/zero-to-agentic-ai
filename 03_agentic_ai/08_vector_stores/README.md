# Module 08 - Vector Stores (Chroma and FAISS)

> **MLCourse - Agentic AI - Vector Stores**

> Stage in the capstone: STORE + RETRIEVE backbone.

A vector store is three things bundled together: your vectors, the metadata
attached to each vector, and an ANN search index that finds approximate nearest
neighbors fast. Module 07 turned chunks into vectors; this module parks them
somewhere queryable. Instead of comparing your question against every chunk
(brute force), the store uses Approximate Nearest Neighbor structures to jump
straight to the promising neighborhood - same idea as a book index letting you
skip to the right page instead of rereading the whole volume.

## What you will learn

1. The anatomy of a vector store: vectors + metadata + ANN search.
2. How Chroma and FAISS differ in persistence, speed, and filtering - side by side.
3. Which store to pick for which situation (a real decision guide).
4. The constructor/query parameters that actually matter for each.
5. The two classic pitfalls: mixing embedders, and forgetting to persist.

## Chroma vs FAISS at a glance

| Aspect | Chroma (`langchain-chroma`) | FAISS (`langchain-community`) |
|---|---|---|
| What it is | An embedded document database with vector search built in | A library of similarity-search indexes (Facebook AI Similarity Search) |
| Persistence model | Auto-persists to disk via `persist_directory` (SQLite-backed); reopen by passing the same path + collection name | No auto-persist; YOU call `save_local()` / `load_local()` to serialize index + docstore to a folder |
| Server-less? | Yes, runs in-process by default (an optional client/server mode exists) | Yes, always fully in-process |
| Speed profile | Fast enough for small/medium corpora; DB conveniences cost some overhead | Extremely fast, SIMD-optimized; multiple index types tuned from thousands to billions of vectors |
| Metadata filtering | Rich `where` filters evaluated at query time (`filter={"chapter": "1"}`) | No native filter support; filter results yourself after retrieval |
| Typical production use | App-local knowledge base: easy persistence, filters, zero infra | High-QPS similarity service behind custom infrastructure; huge-scale search |

Both are server-less here: no daemon, no Docker container, just objects inside
your Python process.

## Decision guide

1. Learning, prototyping, or a small app knowledge base: **Chroma** - persistence
   and metadata filters come free, and reruns are painless.
2. Millions of vectors or a strict latency budget: **FAISS** - its indexes are
   built for exactly that regime.
3. Metadata filtering is central to your queries: **Chroma** today, or FAISS
   paired with your own metadata lookup.
4. You want exotic index tuning (IVF, HNSW, GPU indexes): **FAISS**.
5. Cannot decide yet: start with **Chroma**; migrating later is just re-adding
   documents through the identical LangChain interface.

## Parameters that matter

### Chroma

| Parameter | Meaning | Notes |
|---|---|---|
| `collection_name` | Namespace of vectors inside the database | Reuse it plus `persist_directory` to reopen a store. |
| `persist_directory` | Folder for on-disk storage | Omit it and the store lives only in RAM and dies with the kernel. |
| `embedding` | The `Embeddings` object used for `add` and `query` | Must be the SAME model at both times (module 07 pitfall). |
| `search_kwargs` | Retriever-side knobs, not constructor args | `{"k": 3, "filter": {...}, "fetch_k": 20, "lambda_mult": 0.5}` - relevance cutoffs also live here as `score_threshold`, applied by the retriever layer (module 09). |

### FAISS

| Parameter / concept | Meaning | Notes |
|---|---|---|
| Index type (default: flat) | `IndexFlatL2` exact brute-force L2 search is what `from_documents` builds | Perfect recall, dead simple, fast enough up to ~100k vectors on a laptop. |
| `distance_strategy` | Switches the math: `EUCLIDEAN_DISTANCE` (default) vs `INNER_PRODUCT` (dot) | Use IP with normalized vectors to make dot behave like cosine. |
| Approximate index types | IVF, HNSW, PQ variants trade a little recall for big speed wins at scale | Opt-in territory; flat default is right for learning. |
| `save_local()` / `load_local()` | Serialize index + docstore into a folder | `load_local(..., allow_dangerous_deserialization=True)` - see pitfalls below. |

## When and how

**Reach for a vector store when:** you need semantic search over chunks, RAG
context selection, near-duplicate detection, or "find similar items" features.

**The universal recipe (same for both stores):**

1. Chunk documents (module 06).
2. `Store.from_documents(docs, embedding=embeddings, ...)` - embeds and indexes in one call.
3. Persist deliberately: Chroma via `persist_directory`, FAISS via `save_local()`.
4. Query with `similarity_search(query, k=3)` or `similarity_search_with_score(...)`.
5. Wrap with `.as_retriever()` (module 09) to plug into chains.

## Common pitfalls

- **Mixing embedders between add and query**: index chunks with MiniLM, query
  with nomic, and you get garbage rankings or dimension errors. Vectors from
  different models are coordinates in different spaces - pin one model per store.
- **Forgetting to persist**: a Chroma built without `persist_directory` and a
  FAISS that never saw `save_local()` both evaporate when the notebook kernel
  restarts. FAISS in particular NEVER auto-persists - saving is on you.
- Re-running `from_documents` against an existing persisted collection inserts
  duplicates rather than replacing; wipe the directory (or use explicit ids) on rebuilds.
- Reading Chroma's `_with_score` output as a similarity: it returns a DISTANCE,
  so lower means better - do not compare it directly against cosine numbers.
- Trusting arbitrary `index.pkl` files: loading a FAISS save unpickles data,
  and unpickling executes code. Only load stores you created yourself.

## Contents

| Notebook | What it does |
|---|---|
| `01_chroma_vector_store.nb.py` | Chapter-tagged Alice chunks into persistent Chroma; reopen from disk, scored search, metadata filtering, count(). |
| `02_faiss_vector_store.nb.py` | Same chunks into FAISS; `save_local`/`load_local`, the dangerous-deserialization flag explained honestly, timed searches. |
| `03_chroma_vs_faiss_head_to_head.nb.py` | Identical chunks and queries through both stores; agreement table, latency bars, verdict recap. |

## Summary

Vector stores give module 07's embeddings a durable, searchable home: vectors +
metadata + ANN search. Chroma trades a little raw speed for persistence and
filtering convenience; FAISS trades convenience for raw speed and scale; both
speak the same LangChain interface, so switching is cheap. Pick Chroma while
learning, keep FAISS in your back pocket for scale - then let module 09 hide
the choice behind the retriever abstraction entirely.
