# Module 01: Hybrid Search Strategies

> **MLCourse - RAG Foundations - Advanced Retrieval**

Implement hybrid search by combining sparse (BM25) and dense (embedding-based) retrieval methods, using reciprocal rank fusion to produce superior ranked results over either approach alone.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_bm25_fundamentals](01_bm25_fundamentals.ipynb) | BM25 sparse retrieval: term frequency, inverse document frequency, and indexing |
| 02 | [02_dense_retrieval](02_dense_retrieval.ipynb) | Dense embedding-based retrieval with vector similarity search |
| 03 | [03_reciprocal_rank_fusion](03_reciprocal_rank_fusion.ipynb) | Combining ranked lists from multiple retrievers using RRF |
| 04 | [04_hybrid_rag_pipeline](04_hybrid_rag_pipeline.ipynb) | End-to-end hybrid RAG pipeline merging sparse and dense retrieval |

## Prerequisites

- LangChain modules [07_embeddings](../../01_langchain/07_embeddings/README.md), [08_vector_stores](../../01_langchain/08_vector_stores/README.md), [09_retrievers](../../01_langchain/09_retrievers/README.md) and [10_basic_rag](../../01_langchain/10_basic_rag/README.md)

## When to use this technique

- When keyword precision and semantic understanding are both important
- Datasets with technical terminology, proper nouns, or domain-specific jargon
- Retrieval scenarios where single-method search yields incomplete results
- Production RAG systems requiring robust, high-recall document retrieval
