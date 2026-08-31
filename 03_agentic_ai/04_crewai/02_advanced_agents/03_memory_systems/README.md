# Module 03 - Memory Systems

> **MLCourse - Advanced Agent Features - Memory Systems**

CrewAI's memory systems let agents remember past interactions, learn from previous
runs, and track entity relationships. This module covers short-term, long-term,
and entity memory - the three pillars that make crews adaptive across sessions.

## What you'll learn

- Enable and configure short-term memory for within-run context
- Use long-term memory to persist insights across crew runs
- Track entities and relationships with entity memory
- Combine memory types for cumulative learning
- Reset and manage memory state

## Key concepts

- **Short-term memory**: conversation context within a single kickoff
- **Long-term memory**: persisted learnings across multiple runs
- **Entity memory**: tracking people, places, and concepts mentioned in tasks
- **Memory storage**: how CrewAI stores and retrieves memories
- **Memory configuration**: enabling, disabling, and scoping memory types

## Beginner walkthrough

Think of the three memory types like this:
- **Short-term** = what you remember *during* one conversation. Once the
  conversation ends, it's gone. `short_term_memory.py` shows this using
  `context=[...]` to hand one task's output to the next.
- **Long-term** = what you write down so you remember it *tomorrow*.
  `long_term_memory.py` saves to a real `.db` file on disk — run the file
  twice and the second run will greet you with what the first run learned.
- **Entity memory** = keeping a running notebook of "who/what is this and
  what do I know about it". `entity_memory.py` shows a tiny hand-rolled
  version of that idea.
- `combined_memory_demo.py` puts all three together in one crew run so you
  can see them work side by side.
- `main.py` runs the whole module in order.

Run any file on its own with `python <filename>.py`, or the whole module
with `python main.py`.

## Contents

1. `short_term_memory.py` - within-run context via task-context chaining
2. `long_term_memory.py` - cross-run persistence via SQLite storage
3. `entity_memory.py` - entity tracking, relationship mapping
4. `combined_memory_demo.py` - all three patterns together
5. `main.py` - runs every section above in sequence

Every file runs standalone (`python <file>.py`); `main.py` runs the whole module.
Uses Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`) with local Ollama as fallback.

Note: CrewAI's built-in short-term/entity memory use chromadb, which is broken
in this environment by a conflicting `chromadb-client` package (see
`02_knowledge_sources/README.md`). Long-term memory uses SQLite directly (no
chromadb) and works as CrewAI ships it; short-term/entity memory are
demonstrated with equivalent no-dependency patterns instead.

After this module, continue to `04_reasoning_and_planning` to add reasoning capabilities.
