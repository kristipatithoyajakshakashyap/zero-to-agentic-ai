# Module 07: Cache RAG

> **MLCourse - Advanced RAG - Performance Optimization**

Implement semantic caching in RAG pipelines to avoid redundant retrieval and LLM calls, with intelligent cache invalidation to maintain freshness as underlying data changes.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_semantic_caching](01_semantic_caching.ipynb) | Embedding-based cache lookup for semantically similar queries |
| 02 | [02_cache_invalidation](02_cache_invalidation.ipynb) | TTL, content-based, and event-driven cache invalidation strategies |
| 03 | [03_cache_rag_pipeline](03_cache_rag_pipeline.ipynb) | Full RAG pipeline with multi-level caching for retrieval and generation |

## Prerequisites

- LangChain module [08_vector_stores](../../01_langchain/08_vector_stores/README.md) - semantic cache lookup is a vector search
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on

## When to use this technique

- High-traffic RAG applications where repeated or near-duplicate queries are common
- Cost-sensitive deployments where LLM API calls need to be minimized
- Latency-critical systems requiring sub-second response times for frequent queries
- Applications with slowly changing document collections where caching is effective
