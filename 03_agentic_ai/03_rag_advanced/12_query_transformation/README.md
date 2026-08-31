# Module 12: Query Transformation

> **MLCourse - Agentic AI - Advanced RAG**

Rewrite the question before you search. Every other module in this track improves the *index* or the *ranking*; this one improves the other side of the comparison.

## What the concept is

Retrieval compares a query to documents, and that comparison fails for a reason older than embeddings: the **vocabulary mismatch problem**. The words a user picks are usually not the words the answer is written in.

Dense embeddings fix the *lexical* half of this. They do not fix the deeper half - **question/answer asymmetry**. A question and its answer are different kinds of text: one is short, interrogative and abstract; the other is long, declarative and concrete. Embedding models place text near text that *looks like it*, so a question lands near other questions, not near its answer. Notebook 01 measures this on the real corpus: a rephrasing of the question typically scores *higher* than the passage that actually answers it.

Four families of fix:

| technique | the move | fixes |
|---|---|---|
| **HyDE** | write a hypothetical answer, embed *that* | question/answer asymmetry |
| **Multi-query expansion** | several rephrasings, retrieve with each, fuse the ranks | one phrasing being unlucky |
| **Step-back prompting** | ask a broader question too, retrieve background as well | question too specific for the index |
| **Decomposition** | split a compound question into parts | question needing several documents |

Decomposition is taught in its natural agentic setting at [03_agentic_rag/03_query_decomposition.ipynb](../03_agentic_rag/03_query_decomposition.ipynb) and is deliberately **not** repeated here - these notebooks cross-link to it instead.

## Why it matters

- It fixes **recall** - the case where the right document never entered the candidate set. No reranker can recover a document that was never retrieved.
- It is the correct diagnosis roughly half the time. The other half is a precision problem, which is [11_reranking](../11_reranking/README.md)'s job. Knowing which one you have saves a lot of wasted work.
- Unlike reranking, a transformation **can make results worse** - a hallucinated rewrite drags retrieval somewhere wrong. That asymmetry is why this module insists on measurement.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_transform_queries](01_why_transform_queries.ipynb) | The vocabulary mismatch and question/answer asymmetry |
| 02 | [02_hyde](02_hyde.ipynb) | Generate a hypothetical answer and embed that instead |
| 03 | [03_multi_query_expansion](03_multi_query_expansion.ipynb) | LLM-generated variants plus RRF fusion |
| 04 | [04_step_back_prompting](04_step_back_prompting.ipynb) | Zoom out to retrieve the explaining context |
| 05 | [05_comparing_transformations](05_comparing_transformations.ipynb) | All four on one evaluation set, with cost |

### Walkthrough

**01 - Why transform queries.** Embeds a question alongside an answer-shaped passage, a question-shaped rephrasing, and unrelated text, and shows the rephrasing usually wins. Then runs three progressively more document-like versions of one query through real retrieval and compares precision@5 and first-relevant rank. Ends by laying out the four transformation families and the costs you accept when you adopt any of them (an LLM call on the critical path *before* retrieval, token spend, and a brand-new failure mode).

**02 - HyDE.** Asks Groq for a ~70-word passage in the register of the corpus, then embeds that instead of the question. Explains the counter-intuitive core: the hypothetical answer's *facts do not matter*, only its shape and vocabulary. Shows the similarity scores shifting document by document, then covers multi-sample HyDE (averaging several generations at `temperature=0.7`) and the `alpha`-blended query vector that keeps a foot in both worlds. Closes with a full HyDE RAG loop where the final answer is generated strictly from *retrieved* text - the hypothetical never reaches the user.

**03 - Multi-query expansion.** Generates genuinely different phrasings - varying vocabulary, specificity and grammatical form - always keeping the original in the pool. Fuses the ranked lists with **RRF**, the same algorithm from [01_hybrid_search](../01_hybrid_search/README.md), applied across queries instead of across retrievers. Measures the recall gain (how many documents only the variants found) and then runs a full precision@5 comparison over the shared evaluation questions.

**04 - Step-back prompting.** Generates a deliberately broader version of a specific question, retrieves for both, and combines them as a *union* - specific evidence first, background second. Includes the stronger two-hop variant from the original paper: answer the general question first, then use that as grounding for the specific one. Ends with an honest account of when stepping back actively hurts (already-broad questions, precise lookups).

**05 - Comparing transformations.** Runs baseline, HyDE, multi-query and step-back over the same eight questions with the same keyword-based relevance rules, reporting P@1/3/5, MRR, latency **and LLM calls per query**. Includes per-question win/tie/loss counts, because transformations are high-variance and the mean hides that. Finishes with a decision table mapping symptoms to techniques, and the composition diagram for the full production stack.

## How to run

```bash
# from the repository root
.venv/Scripts/python.exe -m jupyter lab
```

Run the notebooks in order. Each is self-contained and loads `GROQ_API_KEY` from `03_agentic_ai/.env` by walking up the directory tree, so the working directory does not matter.

- **LLM**: Groq, `qwen/qwen3.8-27b`. The free tier is roughly 8000 tokens/minute - and this module spends tokens *before* retrieval, so every loop paces itself and backs off exponentially.
- **Fallback**: local Ollama at `localhost:11434` - substitute `ChatOllama(model="llama3.1:8b")`.
- **Embeddings**: local `all-MiniLM-L6-v2`, downloaded once and cached.
- **Data**: `03_agentic_ai/data/alice.txt`.

## Prerequisites

- [01_hybrid_search](../01_hybrid_search/README.md) - RRF is reused as the fusion step in notebook 03
- [03_agentic_rag](../03_agentic_rag/README.md) - notebook 03 there covers decomposition, the fifth technique in this family
- [11_reranking](../11_reranking/README.md) - the precision-side counterpart; the two are frequently confused
- LangChain [07_embeddings](../../01_langchain/07_embeddings/README.md) and [10_basic_rag](../../01_langchain/10_basic_rag/README.md)

## When to use this technique

- Retrieved chunks are on-topic but never actually answer the question -> **HyDE**
- Results are erratic; small rephrasings change everything -> **multi-query**
- The question asks about a detail inside a larger process -> **step-back**
- The question has several independent parts -> **decomposition**

If the right chunk *is* retrieved but ranked 8th, you have a precision problem and this module is the wrong tool. Use [11_reranking](../11_reranking/README.md).

## Next

[13_contextual_retrieval](../13_contextual_retrieval/README.md) - what if the problem is neither the query nor the ranking, but the chunk itself?
