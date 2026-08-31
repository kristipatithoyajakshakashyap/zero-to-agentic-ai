# Module 14: Graph RAG

> **MLCourse - Agentic AI - Advanced RAG**

Some answers are not written down anywhere. They have to be assembled from facts stated in different places - and that is a job for a graph, not an index.

## What the concept is

Every technique in this track so far assumes **the answer lives inside some chunk**. Find it, hand it to the LLM, done. Reranking finds it more reliably; query transformation finds it when the wording differs; contextual retrieval returns enough of it to be useful.

Graph RAG exists for the questions where that assumption is simply false:

- **Multi-hop** - *"Who owns the cat that told Alice where to find the Hatter?"* needs two facts from two different paragraphs chained together.
- **Aggregation** - *"Which characters appear at both the tea party and the trial?"* is a set intersection over the whole corpus.
- **Relational** - *"What connects the Queen of Hearts to the Mock Turtle?"* is a question about paths in a network.

The alternative representation stores **entities as nodes and relationships as edges**, and answers by *traversing* rather than matching. The multi-hop question becomes a two-edge walk; the aggregation question becomes a set intersection - exact, not approximate, with no threshold to tune.

```
   Duchess ---owns--> Cheshire Cat ---directs Alice to--> Mad Hatter
                                                              |
                                                          attends
                                                              v
                                                       mad tea party
```

## Why it matters

- It covers a class of question the rest of the track structurally cannot answer. Vector search does not merely do these *badly* - it cannot express them.
- It fails in a very different way, and knowing that is half the value: graph retrieval is **exact where it works and returns nothing when entity linking misses**, whereas vector search always returns something plausible.
- It is the clearest illustration in the course that retrieval quality is a *representation* choice, not just a model choice.

Be equally clear about the costs. Extraction is lossy and expensive (one LLM call per chunk); entity resolution is genuinely hard; unconstrained relation vocabularies quietly disconnect the graph; and graphs answer ordinary "what does this passage say" questions badly. Which is why the module ends on a **hybrid**.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_when_vectors_arent_enough](01_when_vectors_arent_enough.ipynb) | Multi-hop, aggregation and relational questions vector search cannot answer |
| 02 | [02_entity_extraction](02_entity_extraction.ipynb) | LLM extraction of entities and relations, with a constrained schema |
| 03 | [03_building_the_graph](03_building_the_graph.ipynb) | NetworkX `MultiDiGraph`, structural diagnostics, Neo4j as the production option |
| 04 | [04_graph_traversal_retrieval](04_graph_traversal_retrieval.ipynb) | Link -> traverse -> verbalise -> generate |
| 05 | [05_hybrid_graph_vector_rag](05_hybrid_graph_vector_rag.ipynb) | Combining structure and content, with routing |

### Walkthrough

**01 - When vectors are not enough.** Runs three hard questions through ordinary dense retrieval and shows the results being *topically plausible and non-answering*, then lets the LLM try anyway so you can watch it either flag the gap or fill it with invention. Rebuilds the same facts as a tiny NetworkX graph and answers both questions by walking edges and intersecting sets. Ends with an honest list of what you give up, and the Docker-free position on Neo4j.

**02 - Entity extraction.** The notebook that decides whether your graph works. Compares an unconstrained extraction prompt against one that fixes entity types, fixes the relation vocabulary, demands canonical names (no pronouns) and demands a strict output format - and explains why `owns` / `has` / `is the owner of` as three separate edges is the single most common Graph RAG failure. Parses defensively and counts rejects as a health metric. Extracts over a sample of passages while **keeping `doc_id` provenance on every triple**, then does entity resolution with normalisation plus an alias map. Ends with an LLM audit that checks sampled triples back against their source paragraph.

**03 - Building the graph.** Explains the three modelling choices (directed, labelled, multi-edge) and why `MultiDiGraph` is the right container. Then the structural diagnostics that matter: degree to find hubs, relation counts to spot schema drift, and - most importantly - **connected components**, because a graph that has silently split into pieces returns empty traversals rather than errors. Covers paths, k-hop neighbourhoods, betweenness centrality, and JSON serialisation. Section 8 shows the equivalent **Cypher** for Neo4j and the `docker run` line, states plainly that **Docker is not required for this course**, and gives a table for when to graduate.

**04 - Graph traversal retrieval.** Builds the three pieces of a graph retriever. **Entity linking** in three flavours - string, embedding, LLM - compared side by side so you can see the cheap ones under-link on paraphrase. **Traversal** with a hop-count study showing 3 hops reaches nearly the whole graph (the graph version of context bloat). **Verbalisation** turning edges into one sentence each. Then path-constrained retrieval, which gives tiny exact context for relational questions - the clearest win over vector search anywhere in this module. Ends by deliberately demonstrating the failure that motivates notebook 05: the graph knows *that* the Caterpillar advised Alice and has no idea *what was said*.

**05 - Hybrid graph + vector RAG.** Puts both context types in one prompt under headings that tell the model which block is quotable and which is derived structure. Runs relational and content questions through graph-only, vector-only and hybrid so the complementarity is visible as a grid. Then adds a **router** that classifies each question RELATIONAL / CONTENT / BOTH and pays only for what it needs - the same idea as [06_adaptive_rag](../06_adaptive_rag/README.md). Closes with a cost table (the dominant term is one LLM call per chunk at index time) and the composed stack showing how the graph sits alongside, not instead of, everything else in this track.

## How to run

```bash
# from the repository root
.venv/Scripts/python.exe -m jupyter lab
```

Run in order. Each notebook is self-contained and loads `GROQ_API_KEY` from `03_agentic_ai/.env` by walking up the directory tree.

- **No Docker, no database, no external service.** Everything runs in-process on NetworkX. Neo4j is shown and explained in notebook 03 as the production upgrade, and is never required.
- **LLM**: Groq, `qwen/qwen3.8-27b`, with backoff and paced loops. Notebook 02 is the token-heaviest (extraction carries a full passage per call) and deliberately samples 8 paragraphs rather than the whole book.
- Notebooks 03-05 use a **curated triple set** extracted in notebook 02 and saved inline, so they do not each re-pay the extraction cost - which is exactly what a real pipeline does, since extraction is a one-off indexing step.
- **Fallback**: local Ollama at `localhost:11434` - `ChatOllama(model="llama3.1:8b")`.
- **Data**: `03_agentic_ai/data/alice.txt`.
- **Generated artifact**: `14_graph_rag/alice_graph.json` (safe to delete).

## Prerequisites

- LangChain [10_basic_rag](../../01_langchain/10_basic_rag/README.md) - you should be comfortable with a plain RAG chain first
- [01_hybrid_search](../01_hybrid_search/README.md) - the vector half of the hybrid in notebook 05
- [03_agentic_rag](../03_agentic_rag/README.md) - tool-using retrieval, the closest sibling to graph traversal
- [05_corrective_rag](../05_corrective_rag/README.md) - the grading idea reused as the extraction audit in notebook 02
- [06_adaptive_rag](../06_adaptive_rag/README.md) - the routing pattern applied in notebook 05
- `networkx` (already in the project environment)

## When to use this technique

- Users ask **multi-hop** questions that chain facts across documents
- Users ask **aggregation** questions - counts, sets, intersections over the corpus
- Your domain is genuinely relational: org charts, supply chains, code dependencies, medical ontologies, incident causality
- You can afford a **one-off LLM call per chunk** to build the graph

Do **not** add a graph when your questions are "what does the documentation say about X". That is most RAG, and vector search already does it better, cheaper and with real citations.

## Next

[10_rag_evaluation](../10_rag_evaluation/README.md) - how to tell whether any of this actually helped, including [05_agent_trajectory_evaluation](../10_rag_evaluation/05_agent_trajectory_evaluation.ipynb) for grading the *steps* an agent took rather than only its answer.
