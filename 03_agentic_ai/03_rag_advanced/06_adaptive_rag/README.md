# Module 06: Adaptive RAG

> **MLCourse - Advanced RAG - Dynamic Strategy Selection**

Classify incoming queries at runtime and dynamically select the optimal RAG strategy—from simple retrieval to multi-step agentic reasoning—based on query complexity and domain.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_query_classification](01_query_classification.ipynb) | Classifying query types: factual, analytical, aggregative, and conversational |
| 02 | [02_strategy_selection](02_strategy_selection.ipynb) | Mapping query classes to retrieval strategies and pipeline configurations |
| 03 | [03_adaptive_rag_pipeline](03_adaptive_rag_pipeline.ipynb) | End-to-end adaptive RAG that dynamically selects the best retrieval and generation path |

## Prerequisites

- LangGraph modules [01_graph_basics](../../02_langgraph/01_graph_basics/README.md) and [02_tool_using_agents](../../02_langgraph/02_tool_using_agents/README.md) - agentic RAG is a graph with a retriever in it
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on
- Modules 03-05 - the strategies this module chooses between at runtime

## When to use this technique

- Systems serving diverse query types that each require different retrieval approaches
- Applications where a single fixed pipeline underperforms across use cases
- Platforms needing to balance latency, cost, and quality based on query difficulty
- Environments where the retrieval strategy should evolve with incoming traffic patterns
