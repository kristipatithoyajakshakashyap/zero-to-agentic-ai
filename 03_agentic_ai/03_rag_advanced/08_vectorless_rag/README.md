# Module 08: Vectorless RAG with Guardrails

> **MLCourse - RAG Foundations - Alternative Retrieval**

Explore retrieval without vector embeddings by leveraging page-level indexing, structured metadata filtering, and guardrails that enforce output quality without relying on similarity search.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_page_index_retrieval](01_page_index_retrieval.ipynb) | Page-level document indexing and retrieval without vector embeddings |
| 02 | [02_structured_metadata](02_structured_metadata.ipynb) | Metadata-based filtering using structured document attributes |
| 03 | [03_guardrails](03_guardrails.ipynb) | Input/output guardrails for content filtering, relevance checking, and safety |
| 04 | [04_vectorless_rag_pipeline](04_vectorless_rag_pipeline.ipynb) | Complete RAG pipeline using non-vector retrieval with guardrail enforcement |

## Prerequisites

- Modules 05-06 (Document processing, text extraction)

## When to use this technique

- Environments where vector embedding infrastructure is unavailable or too costly
- Document collections with rich metadata that enable effective structured retrieval
- Applications requiring deterministic, auditable retrieval without embedding drift
- Systems needing hard guardrails on inputs and outputs beyond semantic similarity
