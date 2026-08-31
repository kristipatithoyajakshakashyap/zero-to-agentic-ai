# Module 02: Multi-Modal RAG

> **MLCourse - RAG Foundations - Multi-Modal Processing**

Extend RAG beyond text by indexing and retrieving across images, tables, and documents using multi-modal embeddings, enabling cross-modal reasoning over heterogeneous data sources.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_image_text_embeddings](01_image_text_embeddings.ipynb) | Joint image-text embedding models for shared vector spaces |
| 02 | [02_multimodal_indexing](02_multimodal_indexing.ipynb) | Indexing strategies for images, tables, and mixed-content documents |
| 03 | [03_cross_modal_retrieval](03_cross_modal_retrieval.ipynb) | Retrieving images from text queries and vice versa |
| 04 | [04_multimodal_rag_pipeline](04_multimodal_rag_pipeline.ipynb) | End-to-end multi-modal RAG pipeline with unified retrieval and generation |

## Prerequisites

- LangChain modules [07_embeddings](../../01_langchain/07_embeddings/README.md), [08_vector_stores](../../01_langchain/08_vector_stores/README.md), [09_retrievers](../../01_langchain/09_retrievers/README.md) and [10_basic_rag](../../01_langchain/10_basic_rag/README.md)

## When to use this technique

- Document collections containing images, charts, diagrams, or tables
- Use cases requiring visual reasoning alongside textual context
- Knowledge bases with mixed media that lose meaning when flattened to text
- Applications like product search, medical imaging reports, or technical manuals
