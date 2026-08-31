# Module 05: Corrective RAG

> **MLCourse - Advanced RAG - Quality Assurance**

Implement quality gates in RAG pipelines that grade retrieved documents, detect hallucinations, and trigger corrective generation when output confidence falls below acceptable thresholds.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_retrieval_grading](01_retrieval_grading.ipynb) | Relevance and quality grading of retrieved documents before generation |
| 02 | [02_hallucination_detection](02_hallucination_detection.ipynb) | Detecting unsupported claims and factual inconsistencies in generated text |
| 03 | [03_corrective_generation](03_corrective_generation.ipynb) | Re-generation strategies when initial output fails quality checks |
| 04 | [04_corrective_rag_pipeline](04_corrective_rag_pipeline.ipynb) | End-to-end corrective RAG pipeline with retrieval grading and hallucination checks |

## Prerequisites

- LangGraph modules [01_graph_basics](../../02_langgraph/01_graph_basics/README.md) and [02_tool_using_agents](../../02_langgraph/02_tool_using_agents/README.md) - agentic RAG is a graph with a retriever in it
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on

## When to use this technique

- Production systems requiring factual accuracy guarantees
- High-stakes domains (medical, legal, financial) where hallucinations are costly
- Applications where retrieval quality varies and filtering is essential
- Pipelines that need automated quality feedback loops
