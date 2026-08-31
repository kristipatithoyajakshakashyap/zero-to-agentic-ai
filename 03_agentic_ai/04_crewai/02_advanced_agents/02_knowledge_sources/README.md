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

## Beginner walkthrough

New to "grounding"? It just means: giving the model facts it can read
before it answers, instead of trusting whatever it remembers from
training. Without grounding, an LLM might guess or make things up. With
grounding, you can ask it a question whose answer only exists in *your*
document, and it will get it right because the text is right there in
front of it.

- Start with `text_knowledge_source.py` — the simplest case: one agent,
  one text file, one question that can only be answered correctly by
  reading the file.
- `pdf_knowledge_source.py` shows the same idea with a real PDF, using
  `pypdf` to pull the text out first (LLMs can't read PDF bytes directly).
- `agent_vs_crew_knowledge.py` teaches *scoping*: should every agent on
  your team see a piece of information, or just one of them? Run it and
  compare how the two agents answer the same style of question.
- `direct_retrieval.py` strips away the Agent/Task/Crew machinery
  entirely — sometimes you just want one grounded answer, not a whole
  crew.
- `main.py` runs all four in order so you can see the whole module story
  end to end.

Run any file on its own with `python <filename>.py`, or the whole module
with `python main.py`.

## Contents

1. `text_knowledge_source.py` - grounding an agent with a text file
2. `pdf_knowledge_source.py` - grounding an agent with a PDF document
3. `agent_vs_crew_knowledge.py` - private agent knowledge vs shared crew knowledge
4. `direct_retrieval.py` - grounding a single LLM call without a crew
5. `main.py` - runs every section above in sequence

Every file runs standalone (`python <file>.py`); `main.py` runs the whole module.
Uses Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`) with local Ollama as fallback.

Note: this environment has a conflicting `chromadb-client` package that breaks
CrewAI's built-in vector-backed `knowledge_sources` (it forces ChromaDB into
thin-client mode). Rather than touch the shared `chromadb` install, these
scripts load document text directly into agent context - same practical
grounding effect, no vector store required.

After this module, continue to `03_memory_systems` to add persistent memory.
