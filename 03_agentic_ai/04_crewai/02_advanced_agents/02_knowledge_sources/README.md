# Module 02 - Knowledge Sources

> **MLCourse - Advanced Agent Features - Knowledge Sources**

Agents are only as good as what they know. CrewAI supports knowledge sources that
give agents access to text files, PDFs, and other documents without relying on
external RAG pipelines. This module covers agent-level and crew-level knowledge
configuration.

## What you'll learn

- Attach text and PDF knowledge sources to agents
- Configure knowledge at the agent level vs the crew level
- Control how knowledge is retrieved and injected into prompts
- Combine knowledge sources with tools for hybrid retrieval
- Manage knowledge lifecycle and updates

## Key concepts

- **Knowledge source**: a document or dataset an agent can access
- **Agent knowledge**: knowledge scoped to a single agent
- **Crew knowledge**: shared knowledge across all agents in a crew
- **Knowledge retrieval**: how relevant chunks are selected
- **File knowledge**: text files loaded directly as context

## Contents

1. `01_text_knowledge.ipynb` - TextFileKnowledgeSource, inline text
2. `02_pdf_knowledge.ipynb` - PDF knowledge, file-based sources
3. `03_agent_vs_crew_knowledge.ipynb` - scope differences, when to use each

After this module, continue to `03_memory_systems` to add persistent memory.
