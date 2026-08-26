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

- Modules 02-03 (Agent design, tool use), Module 01 (Hybrid search)

## When to use this technique

- Systems serving diverse query types that each require different retrieval approaches
- Applications where a single fixed pipeline underperforms across use cases
- Platforms needing to balance latency, cost, and quality based on query difficulty
- Environments where the retrieval strategy should evolve with incoming traffic patterns
