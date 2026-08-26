# Module 15: Persistence & Checkpointing

> **MLCourse - Agentic AI - LangGraph**

Saving and restoring agent state across invocations — from in-memory checkpoints to durable SQLite/Postgres backends, time-travel debugging, and cross-thread memory.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_memory_saver](01_memory_saver.ipynb) | Using `MemorySaver` for quick in-memory checkpointing during development |
| 02 | [02_sqlite_postgres](02_sqlite_postgres.ipynb) | Persistent storage with `SqliteSaver` and `PostgresSaver` for production use |
| 03 | [03_time_travel](03_time_travel.ipynb) | Replaying past states, branching from checkpoints, and debugging with time travel |
| 04 | [04_cross_thread_memory](04_cross_thread_memory.ipynb) | Sharing memory across conversation threads with checkpoint namespaces |

## Prerequisites

- Module 14 (Tool-Using Agents)

## What you'll learn

- How LangGraph checkpointers automatically persist graph state after every step
- How to swap backends from `MemorySaver` to `SqliteSaver` or `PostgresSaver`
- How to time-travel through execution history by replaying and branching from checkpoints
- How to implement cross-thread memory for long-running or multi-session agents
