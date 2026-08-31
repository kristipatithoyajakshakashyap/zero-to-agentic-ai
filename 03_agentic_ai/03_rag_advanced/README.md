# Advanced RAG Techniques

Basic RAG is one straight line: embed the question, fetch the top-k chunks, paste
them into a prompt. It works until it doesn't — the query is worded badly, the
answer lives in an image, one retrieval round isn't enough, the retrieved chunks
are irrelevant and the model confidently invents an answer anyway.

Each module here fixes one of those failure modes, and every module ends in a
runnable `*_rag_pipeline` notebook so you see the fix working end to end rather
than as a snippet.

## Where each module attacks the pipeline

```
QUERY  ->  RETRIEVE  ->  RERANK  ->  GRADE  ->  GENERATE  ->  MEASURE
  |           |             |          |           |             |
 03,06       01,02,        11         05,08       04,09          10
 12          13,14
 rewrite,    hybrid,       cross-     grade &     self-correct   metrics,
 HyDE,       multimodal,   encoder    guardrail   & remember     RAGAS,
 decompose   chunking,     precision                             human,
             graph                                               trajectory

  07 (caching) wraps the whole thing to make repeats fast and cheap
```

The two most common diagnoses, and where they send you:

- **The right document was never retrieved** - a *recall* problem. Go to
  [12_query_transformation](./12_query_transformation/README.md),
  [13_contextual_retrieval](./13_contextual_retrieval/README.md), or
  [01_hybrid_search](./01_hybrid_search/README.md).
- **The right document was retrieved but ranked 8th** - a *precision* problem.
  Go to [11_reranking](./11_reranking/README.md).

## Modules (canonical learning order)

| Folder | Step | Teaches |
|---|---|---|
| [01_hybrid_search](./01_hybrid_search/README.md) | 1 | BM25 sparse retrieval · dense retrieval · reciprocal rank fusion · hybrid pipeline |
| [02_multimodal_rag](./02_multimodal_rag/README.md) | 2 | Joint image-text embeddings · multimodal indexing · cross-modal retrieval |
| [03_agentic_rag](./03_agentic_rag/README.md) | 3 | Agent-driven retrieval · self-querying metadata filters · query decomposition |
| [04_autonomous_rag](./04_autonomous_rag/README.md) | 4 | Self-routing between strategies · self-correction · an autonomous reasoning loop |
| [05_corrective_rag](./05_corrective_rag/README.md) | 5 | Grading retrieved docs · hallucination detection · corrective re-generation |
| [06_adaptive_rag](./06_adaptive_rag/README.md) | 6 | Query classification · picking a strategy per query · adaptive pipeline |
| [07_cache_rag](./07_cache_rag/README.md) | 7 | Semantic cache lookup · TTL and event-driven invalidation · multi-level caching |
| [08_vectorless_rag](./08_vectorless_rag/README.md) | 8 | Page-index retrieval without embeddings · metadata filtering · guardrails |
| [09_persistent_memory_rag](./09_persistent_memory_rag/README.md) | 9 | Long-term memory · conversational RAG · knowledge that survives sessions |
| [10_rag_evaluation](./10_rag_evaluation/README.md) | 10 | Precision/recall/faithfulness metrics · RAGAS · human evaluation · agent trajectory evaluation |
| [11_reranking](./11_reranking/README.md) | 11 | Bi-encoder vs cross-encoder · retrieve-then-rerank · measuring the real precision lift · latency and cost |
| [12_query_transformation](./12_query_transformation/README.md) | 12 | Vocabulary mismatch · HyDE · multi-query expansion · step-back prompting |
| [13_contextual_retrieval](./13_contextual_retrieval/README.md) | 13 | The small-to-big problem · parent document retriever · sentence windows · contextual chunk headers |
| [14_graph_rag](./14_graph_rag/README.md) | 14 | Multi-hop and relational questions · entity extraction · NetworkX graphs · hybrid graph + vector RAG |
| [15_late_interaction_retrieval](./15_late_interaction_retrieval/README.md) | 15 | ColBERT / late interaction · token-level embeddings · MaxSim scoring · storage/latency cost vs bi-encoder and cross-encoder |

The order is a build order, not a ranking: 01 gives you the retriever the later
modules improve on, and 10 gives you the scoreboard that tells you whether any of
those improvements actually helped. Modules 11-14 are the technique upgrades you
apply *to* that baseline once you can measure it - which is why they come after
the evaluation module rather than before it.

If you only have time for three, do 01, 10, and 11. If you have time for five,
add 05 and 12.

## Prerequisites

- [**01_langchain**](../01_langchain/README.md) — especially
  [07_embeddings](../01_langchain/07_embeddings/README.md),
  [08_vector_stores](../01_langchain/08_vector_stores/README.md),
  [09_retrievers](../01_langchain/09_retrievers/README.md), and
  [10_basic_rag](../01_langchain/10_basic_rag/README.md). You should be able to
  build a plain RAG chain before you start improving one.
- [**02_langgraph**](../02_langgraph/README.md) — modules 03, 04, 05, 06 and 09
  are graphs with retrieval in them, so `StateGraph` and tool-calling should feel
  familiar.

## Providers and keys

Same local-first rule as the rest of the track:

- **Ollama** (`ChatOllama`) — free and local, no key needed.
- **Groq** (`ChatGroq`) — free-tier cloud key, used for the grading, routing, and
  classification calls where a faster model keeps the loops snappy.
- Embeddings are local HuggingFace models (no key) unless a notebook says otherwise.

`GROQ_API_KEY` lives in `03_agentic_ai/.env` (copy `.env.example`). Modules 01-10
guard their key-dependent cells: without a key they print setup instructions and
skip, so the notebooks still execute top-to-bottom.

Modules **11-14** take a different approach on purpose. They find the `.env` by
walking up the directory tree from wherever the notebook is opened, and they
contain **no skip branches** - every saved output is a real Groq response on real
data. They use `qwen/qwen3.8-27b`, and because the Groq free tier is roughly
**8000 tokens per minute**, every loop that calls the model paces itself and
retries with exponential backoff. The documented offline fallback is a local
Ollama server at `localhost:11434`: swapping `ChatGroq` for
`ChatOllama(model="llama3.1:8b")` is the only change required.

## Setup

```powershell
copy ..\.env.example ..\.env    # then paste your Groq key
winget install Ollama.Ollama
ollama pull llama3.2
pip install langchain-chroma rank-bm25 sentence-transformers ragas networkx
```

Modules 11-14 additionally download two small local models on first run
(`all-MiniLM-L6-v2` and `cross-encoder/ms-marco-MiniLM-L-6-v2`, ~80 MB each,
cached afterwards). No database and **no Docker** is required anywhere in this
track - `14_graph_rag` runs entirely in memory on NetworkX and shows Neo4j only
as the production option.

## Data this track uses

Shared corpora live in [`../data/`](../data):

| File | Used by |
|---|---|
| `alice.txt` | most modules — the default text corpus for indexing and querying |
| `attention_is_all_you_need.pdf` | the PDF/page-structure demos, notably 08_vectorless_rag |
| `multimodal_images/` | 02_multimodal_rag — the image side of cross-modal retrieval |

## Generated artifacts

Running the notebooks writes local files you can safely delete to start fresh:

- `01_hybrid_search/chroma_store`, `chroma_rag`, `chroma_rrf` — persisted Chroma indexes
- `../data/chroma_multimodal` — the multimodal index from module 02
- `10_rag_evaluation/ragas_results.json`, `human_eval_results.json`,
  `evaluation_pipeline_results.json` — saved evaluation scores
- `14_graph_rag/alice_graph.json` — the serialised knowledge graph
