# Module 09: Persistent Memory RAG

> **MLCourse - Advanced RAG - Long-Term Context**

Build RAG systems with persistent memory that retain conversation history, accumulate knowledge across sessions, and maintain contextual coherence in extended multi-turn interactions.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_long_term_memory](01_long_term_memory.ipynb) | Long-term memory storage and retrieval for cross-session knowledge persistence |
| 02 | [02_conversational_rag](02_conversational_rag.ipynb) | Conversational RAG with chat history integration and context window management |
| 03 | [03_persistent_rag_pipeline](03_persistent_rag_pipeline.ipynb) | End-to-end persistent memory RAG with session continuity and knowledge accumulation |

## Prerequisites

- LangChain module [11_memory_and_state](../../01_langchain/11_memory_and_state/README.md) - the session-id history pattern
- LangGraph module [03_persistence_checkpointing](../../02_langgraph/03_persistence_checkpointing/README.md) - durable state across sessions
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on

## When to use this technique

- Customer support systems that need to remember prior interactions
- Personalized assistants that accumulate user preferences over time
- Research tools that build on previous queries and findings across sessions
- Applications requiring continuity in multi-session knowledge work
