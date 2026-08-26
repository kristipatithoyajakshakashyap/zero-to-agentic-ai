# Advanced RAG Techniques

Go beyond basic retrieval-augmented generation. Explore multi-stage retrieval
pipelines, query transformation, reranking, hybrid search, evaluation
frameworks, and production-grade patterns for building robust RAG systems that
handle real-world complexity.

## Modules

| Folder | Teaches |
|---|---|
| [01_query_transformations](./01_query_transformations/README.md) | HyDE, query rewriting, step-back prompting, sub-question decomposition |
| [02_advanced_chunking](./02_advanced_chunking/README.md) | Semantic chunking, agentic chunking, context-aware splitting |
| [03_hybrid_search](./03_hybrid_search/README.md) | Combining dense + sparse retrieval, BM25 + vector search |
| [04_reranking](./04_reranking/README.md) | Cross-encoder reranking, Cohere rerank, ColBERT |
| [05_multi_hop_rag](./05_multi_hop_rag/README.md) | Iterative retrieval, chain-of-thought reasoning across documents |
| [06_graph_rag](./06_graph_rag/README.md) | Knowledge graph augmentation, entity extraction, GraphRAG |
| [07_self_rag](./07_self_rag/README.md) | Self-reflective retrieval, relevance grading, hallucination detection |
| [08_rag_evaluation](./08_rag_evaluation/README.md) | RAGAS, DeepEval, faithfulness and relevance metrics |
| [09_production_patterns](./09_production_patterns/README.md) | Caching, observability, guardrails, streaming, error recovery |
| [10_capstone_advanced_rag](./10_capstone_advanced_rag/README.md) | End-to-end advanced RAG application with evaluation pipeline |

## Prerequisites

Complete **LangChain Fundamentals** before starting this section.
A solid grasp of embeddings, vector stores, and basic RAG is assumed.
