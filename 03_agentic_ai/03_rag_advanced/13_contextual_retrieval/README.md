# Module 13: Contextual Retrieval

> **MLCourse - Agentic AI - Advanced RAG**

Stop assuming the unit you *search* has to be the unit you *read*.

## What the concept is

Chunking contains a tension that no reranker or query rewrite can resolve - the **small-to-big problem**:

- **Small chunks retrieve well.** A two-sentence chunk is about one thing, so its embedding is sharp and its similarity score is meaningful.
- **Small chunks answer badly.** They rarely carry enough surrounding detail, and they lose the antecedent of every pronoun in them.
- **Large chunks answer well** but **retrieve badly** - a page is about five things, so its embedding is the average of five topics and matches nothing sharply.

Tuning chunk size just picks a point on that tradeoff. The actual fix is to **decouple the retrieval unit from the generation unit**:

| technique | search over | give the LLM |
|---|---|---|
| **Parent document retriever** | small child chunks | the whole parent document |
| **Sentence window** | single sentences | the sentence plus N neighbours |
| **Contextual chunk headers** | chunk *plus a generated context header* | the chunk (header optional) |

The first two change what you **return**. The third changes what you **embed**. They are independent and they compose.

## Why it matters

- It is the difference between "the retriever found the right region" and "the LLM could actually answer from it".
- Contextual headers address a failure that is otherwise invisible: chunks whose subject was cut away are **unretrievable**, no matter how good your embedding model is. Anthropic published a version of this in 2024 and reported large reductions in retrieval failure.
- It interacts directly with [11_reranking](../11_reranking/README.md): rerank the small units (they fit the cross-encoder's 512-token window), then expand to the big ones.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_small_to_big_problem](01_small_to_big_problem.ipynb) | Why precise chunks retrieve well and answer badly |
| 02 | [02_parent_document_retriever](02_parent_document_retriever.ipynb) | LangChain `ParentDocumentRetriever`: child index + parent docstore |
| 03 | [03_sentence_window_retrieval](03_sentence_window_retrieval.ipynb) | Index sentences, return the match plus its neighbours |
| 04 | [04_contextual_chunk_headers](04_contextual_chunk_headers.ipynb) | Prepend situating context before embedding |
| 05 | [05_comparing_granularity](05_comparing_granularity.ipynb) | All four strategies measured, with context cost |

### Walkthrough

**01 - The small-to-big problem.** Builds three indexes over the same text at 200, 600 and 1500 characters, and shows the two halves of the tradeoff directly: small chunks produce the highest top-hit cosine, and the worst answers. Then finds the concrete reason - counts how many small chunks *open with an unresolved pronoun*, chunks that are retrievable and useless because you cannot tell who "she" is.

**02 - Parent document retriever.** Builds the mechanism by hand in twenty lines first (search children, dedupe by parent, return parents ranked by their best child), then swaps in LangChain's `ParentDocumentRetriever` with a Chroma child index and an `InMemoryStore` docstore. Covers the three-level variant with a `parent_splitter` for when source documents are too big to return whole, and ends with the same question answered from children vs parents. Notes the LangChain 1.x import paths (`langchain_classic.retrievers`, `langchain_core.stores`).

**03 - Sentence window retrieval.** Splits the corpus into one flat *ordered* list of sentences - the window is defined by position, so order is load-bearing. Implements the window with an overlap guard (three matches in one passage would otherwise burn three context slots on the same text) and shows sentences giving the sharpest top-hit cosine of any granularity. Tunes the window from 0 to 8 and reads the resulting answers. Ends with the production-shaped version: sentences carry a `doc_id` and the window is clamped so it can never splice the end of one document onto the start of another.

**04 - Contextual chunk headers.** Finds the real orphan chunks in the corpus (no character or place named anywhere in them), then builds two kinds of header: **static** ones derived from document structure - free, no LLM - and **LLM-generated** ones that resolve pronouns and name the participants. Compares plain vs static vs LLM embeddings on probe queries. Ends with the design choice people miss: the header helped *retrieval*, but whether it belongs in the *prompt* is a separate decision - so embed the headed version, store both, return whichever suits.

**05 - Comparing granularity.** Runs all four strategies over eight questions with identical keyword-based relevance rules, reporting precision@3, **hit rate**, mean context size, and - the column people forget - **hit rate per 1000 characters**. Returning more text almost always raises hit rate; in the limit, returning the whole book scores 1.0 and is useless. Ends with a corpus-shape-to-strategy table and the composed production stack.

## How to run

```bash
# from the repository root
.venv/Scripts/python.exe -m jupyter lab
```

Run in order. Each notebook is self-contained and finds `GROQ_API_KEY` in `03_agentic_ai/.env` by walking up the directory tree.

- **LLM**: Groq, `qwen/qwen3.8-27b`, with exponential backoff and paced loops for the ~8000 tokens/minute free tier. Notebook 04 is the token-heaviest (one call per sampled chunk) and deliberately samples rather than heading the whole corpus.
- **Fallback**: local Ollama at `localhost:11434` - `ChatOllama(model="llama3.1:8b")`.
- **Embeddings**: local `all-MiniLM-L6-v2`.
- **Data**: `03_agentic_ai/data/alice.txt`.

## Prerequisites

- LangChain [08_vector_stores](../../01_langchain/08_vector_stores/README.md) and [09_retrievers](../../01_langchain/09_retrievers/README.md) - `Chroma` and the retriever interface
- LangChain [10_basic_rag](../../01_langchain/10_basic_rag/README.md) - text splitters and the basic chain
- [11_reranking](../11_reranking/README.md) - notebook 02 there explains the cross-encoder truncation limit that makes "rerank children, return parents" the right order

## When to use this technique

- Answers are incomplete even though retrieval found the right area -> **parent document** or **sentence window**
- Your corpus is flowing prose, transcripts or books -> **sentence window**
- Your corpus has real structure - sections, tickets, pages -> **parent document**
- Chunks lose their subject when split (pronouns, "the above", bare tables) -> **contextual headers**
- Short self-contained records like FAQs or product entries -> you do not have this problem; fixed chunks are fine

## Next

[14_graph_rag](../14_graph_rag/README.md) - what to do when the answer is not in any single chunk at all.
