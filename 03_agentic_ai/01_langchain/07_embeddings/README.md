# Module 07 - Embeddings

> **MLCourse - Agentic AI - Embeddings**

> Stage in the capstone: EMBED - every chunk becomes a vector; query becomes one too.

An embedding is a function that turns text into a fixed-length list of floats (a
vector) whose *geometry* encodes *meaning*. Texts that talk about the same thing
land close together in this space; unrelated texts land far apart. "How do I
reset my password?" ends up neighbors with "I forgot my login credentials" even
though the two sentences share almost no words. That is exactly the superpower
the capstone chatbot needs: it lets retrieval match a user's question to your
documents by MEANING instead of by keyword overlap.

## What you will learn

1. What an embedding is and why agents cannot do semantic search without them.
2. The two similarity formulas everyone uses (cosine and dot product) - kept simple.
3. How dimensionality differs across the three models this track touches.
4. The free-vs-paid trade-off table, so you can choose deliberately.
5. The `embed_documents` vs `embed_query` split, and the pitfalls that silently
   corrupt vector search when you get it wrong.

## Similarity math, kept simple

Given vectors `a` and `b` of the same dimension:

| Measure | Formula | Reads as | Range |
|---|---|---|---|
| Dot product | `dot(a, b) = sum(a_i * b_i)` | Alignment scaled by both lengths | Unbounded |
| Cosine | `cos(a, b) = dot(a, b) / (norm(a) * norm(b))` | Angle between directions only | -1 to 1 |

- **Cosine** ignores how LONG each vector is and compares direction only. For
  text embeddings this is usually what you want: a longer paragraph should not
  score higher just because it has more words.
- **Dot** is cheaper (no normalization) but conflates "related" with "large
  magnitude", so rankings can drift.
- **Key identity**: if both vectors are normalized to unit length, then
  `dot == cosine`. Many stacks (FAISS `IndexFlatIP`, normalized Chroma spaces)
  exploit this. When in doubt, normalize explicitly before comparing.
- Embedding vectors are mostly positive numbers, so in practice cosine scores
  hover between 0 (unrelated) and 1 (near-duplicate) rather than using the full
  -1 to 1 range.

## Dimensionality of the models used in this track

| Model | Provider / access | Dims | Keyless? |
|---|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace, runs locally via `HuggingFaceEmbeddings` | 384 | Yes |
| `nomic-embed-text` | Ollama, runs locally via `OllamaEmbeddings` | 768 | Yes (needs Ollama installed) |
| `text-embedding-3-small` | OpenAI API via `OpenAIEmbeddings` | 1536 | No (`OPENAI_API_KEY`) |

More dimensions means more nuance per vector, but also more memory, larger
indexes, and slower distance computations. MiniLM's 384 dims are genuinely good
enough for learning, prototyping, and even many production workloads.

## Free vs paid trade-offs

| Aspect | Free local (MiniLM, nomic) | Paid API (OpenAI 3-small) |
|---|---|---|
| Cost | $0 forever | ~$0.02 per 1M tokens (tiny for demos; adds up at corpus scale) |
| Privacy | Text never leaves your machine | Every embedded string is sent to the vendor |
| Internet | Only the first model download | Required on every call |
| Latency | Milliseconds, no network hop | Network round trip per request |
| Quality | Strong English baseline | Stronger, notably better multilingual |
| Rate limits | None - it is your own CPU | Vendor quotas and billing |

## When to reach for which

**Free local embedders win when:**

- You are learning or prototyping (this course, honestly).
- Data is sensitive and must stay on-device (health, legal, internal docs).
- You need offline or air-gapped operation.
- You are embedding huge corpora where per-token cost would compound.

**A paid API wins when:**

- Retrieval quality is the product and marginal gains matter.
- Your corpus is multilingual beyond MiniLM's comfort zone.
- You already have a provider relationship, keys, and budget dashboards.

## How embeddings flow through LangChain

Every embedder object exposes exactly the two methods you need:

| Method | Input | Used at | Example call count |
|---|---|---|---|
| `embed_documents(list[str])` | Whole corpus chunks | INDEX time (module 08) | Once per chunk |
| `embed_query(str)` | One search string | QUERY time (every question) | Once per question |

The output is always `list[float]` of the model's dimensionality. Module 08
feeds these vectors into Chroma/FAISS; module 09 wraps the store as a retriever;
the capstone calls `embed_query` on every user turn.

> **Bold rule**: index-time and query-time must use THE SAME MODEL, or you are
> comparing coordinates from two different universes.

## Common pitfalls

- **Forgetting normalization when mixing cosine and dot math**: dot favors
  high-magnitude vectors, so raw-dot rankings can quietly differ from
  cosine rankings. Normalize once, then either formula agrees.
- **Model mismatch between index time and query time**: indexing chunks with
  MiniLM but querying with nomic does not raise an error if dimensions happen
  to align through some wrapper - it just returns confidently wrong results.
  Store the model name beside the index and assert on load.
- Assuming all embedders share one dimensionality: passing MiniLM-sized slots a
  1536-dim vector crashes loudly (a gift); some mismatches fail silently (a trap).
- Re-embedding on every run during development: cache vectors or persist stores,
  or you pay the same compute repeatedly while iterating.

## Contents

| Notebook | What it does |
|---|---|
| `01_free_embeddings_intuition.nb.py` | MiniLM (384-dim): three sentences, hand-computed cosine matrix, heatmap, batch embedding, optional Ollama nomic (768-dim) rerun. |
| `02_openai_embeddings.nb.py` | `text-embedding-3-small` (1536-dim), key-guarded, mirrors notebook 01 to prove the swap pattern, with real cost math. |

## Summary

Embeddings convert text into geometry: closeness becomes relatedness, which is
what makes semantic search, dedup, RAG context selection, and most agent memory
possible. Cosine similarity (normalized dot product) is the number to read, 384
free local dimensions are enough to learn everything, and the free-vs-paid
choice is a trade-off table - not a moral decision. Next module gives those
vectors somewhere to live and a fast way to be searched: vector stores.
