# Module 04: Autonomous RAG

> **MLCourse - Advanced RAG - Self-Governing Systems**

Build RAG systems that autonomously route queries, self-correct retrieval failures, and manage multi-step reasoning loops without explicit external orchestration.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_self_routing](01_self_routing.ipynb) | Query routing to select retrieval strategies, web search, or direct LLM response |
| 02 | [02_self_correction](02_self_correction.ipynb) | Detecting and recovering from retrieval failures and low-quality generations |
| 03 | [03_autonomous_loop](03_autonomous_loop.ipynb) | Full autonomous reasoning loop with self-evaluation and termination conditions |

## Prerequisites

- LangGraph modules [01_graph_basics](../../02_langgraph/01_graph_basics/README.md) and [02_tool_using_agents](../../02_langgraph/02_tool_using_agents/README.md) - agentic RAG is a graph with a retriever in it
- Module 03 ([Agentic RAG](../03_agentic_rag/README.md)) - the agent loop this module makes self-governing

## When to use this technique

- Open-ended applications where query type cannot be predicted in advance
- Systems requiring resilience against retrieval noise and irrelevant context
- Scenarios where the pipeline must decide its own execution path
- Production systems that need minimal human intervention across diverse query types
