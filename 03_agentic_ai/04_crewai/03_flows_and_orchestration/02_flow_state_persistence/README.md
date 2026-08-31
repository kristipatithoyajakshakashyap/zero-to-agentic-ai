# 02 — Flow State Persistence

## What is this, and why does it matter?

By default a Flow's state only exists in memory while your Python script is
running. If the process crashes, or the flow needs to pause and wait for
something (a human, a webhook, tomorrow), you lose everything.
**Persistence** solves this: CrewAI's `@persist` decorator automatically
saves your flow's state to a local SQLite database after every step, keyed
by a unique flow id. Later, you can create a new Flow instance with that
same id and CrewAI loads the saved state instead of starting over.

This matters for anything long-running or resumable — a workflow that waits
for approval, a multi-day research pipeline, or just being able to recover
from a crash without redoing expensive LLM calls.

## Files in this module

| File | What it teaches |
|---|---|
| `persisted_flow.py` | A 2-step Flow (`brainstorm` -> `plan`) decorated with `@persist`, so every run's state is checkpointed to SQLite automatically. |
| `checkpoint_inspection.py` | Reads a saved checkpoint directly from SQLite, then creates a new Flow instance with the same id to demonstrate resuming from that checkpoint. |
| `main.py` | Runs both files above in sequence. |

## Walkthrough

1. **`persisted_flow.py`** — `ChecklistFlow` is decorated with `@persist`.
   Nothing else changes about how you write the flow's steps — CrewAI
   handles saving state behind the scenes. `run_and_checkpoint()` generates
   a fresh UUID as the flow id, runs the flow, and prints where it got
   checkpointed. CrewAI's default persistence backend is SQLite; find the
   database location any time via `SQLiteFlowPersistence().db_path`.

2. **`checkpoint_inspection.py`** — `inspect_checkpoint(flow_id)` reads the
   raw saved row for a flow id straight out of SQLite, so you can see
   exactly what's stored. `resume_flow(flow_id)` then creates a **new**
   `ChecklistFlow()` object and calls `kickoff()` with that same id — this
   is what makes CrewAI load the existing state instead of starting fresh.

3. **`main.py`** — runs a full checkpoint-then-resume cycle, printing the
   idea and plan before and after resuming, so you can confirm they match.

## How to run it

```bash
python persisted_flow.py         # create + checkpoint one flow run
python checkpoint_inspection.py  # checkpoint, inspect, then resume
python main.py                   # both, in sequence
```

Uses your Groq API key from `03_agentic_ai/.env` (`GROQ_API_KEY`), with a
local Ollama fallback. No OpenAI is used anywhere in this course.
