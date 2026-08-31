# Module 03: Agentic RAG

> **MLCourse - Advanced RAG - Agent-Driven Retrieval**

Augment RAG with an agent that actively decides what to retrieve, how to reformulate queries, and whether additional retrieval rounds are needed before generating a final answer.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_agent_driven_retrieval](01_agent_driven_retrieval.ipynb) | Agent-based retrieval orchestration with iterative decision-making |
| 02 | [02_self_querying](02_self_querying.ipynb) | Self-querying mechanisms for automatic structured filter extraction |
| 03 | [03_query_decomposition](03_query_decomposition.ipynb) | Breaking complex queries into sub-questions for targeted retrieval |
| 04 | [04_agentic_rag_pipeline](04_agentic_rag_pipeline.ipynb) | Full agentic RAG pipeline with retrieval planning and adaptive execution |

## Prerequisites

- LangGraph modules [01_graph_basics](../../02_langgraph/01_graph_basics/README.md) and [02_tool_using_agents](../../02_langgraph/02_tool_using_agents/README.md) - agentic RAG is a graph with a retriever in it
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on

## When to use this technique

- Complex questions that require multi-hop reasoning across documents
- Queries where initial retrieval is insufficient and follow-up searches are needed
- Systems that benefit from dynamic retrieval strategies over fixed pipelines
- Applications requiring query understanding and reformulation before retrieval
