# 03 — Human in the Loop

## What is this, and why does it matter?

AI agents can be confidently wrong. "Human in the loop" (HITL) means the
workflow pauses at a key point and waits for a real person to approve,
reject, or edit the AI's output before anything irreversible happens
(sending a message, spending money, publishing content). It's one of the
simplest and most effective safety mechanisms you can add to an agentic
system.

## Files in this module

| File | What it teaches |
|---|---|
| `hitl_flow.py` | A Flow-level approval gate: draft -> approve/reject -> finalize, using a dedicated flow step as the checkpoint. |
| `task_level_human_input.py` | CrewAI's built-in `human_input=True` task flag, which pauses after a single task for reviewer feedback. |
| `main.py` | Runs both files above in sequence. |

## Walkthrough

1. **`hitl_flow.py`** — `HumanApprovalFlow` has three steps: `draft_proposal`
   (an agent writes a one-sentence proposal), `gate_on_approval` (the
   approval checkpoint), and `finalize` (only runs its LLM call if
   approved). The `auto_approve()` function stands in for a real human
   click/reply so this course can run unattended — swap it for an
   `input()`-based prompt to make it truly interactive.

2. **`task_level_human_input.py`** — Shows the other, more built-in way to
   add a human checkpoint: CrewAI's `Task(human_input=True)` flag, which
   pauses the crew and calls Python's `input()` to collect feedback after
   that task runs. Since `input()` would block this course's automated
   runs, this file demonstrates the same reviewer-loop pattern explicitly
   via a `reviewer_feedback()` stand-in function, so it stays runnable
   end-to-end while showing the exact same concept.

3. **`main.py`** — runs both approval patterns back to back.

## How to run it

```bash
python hitl_flow.py                 # flow-level approval gate
python task_level_human_input.py    # task-level human_input pattern
python main.py                      # both, in sequence
```

Uses your Groq API key from `03_agentic_ai/.env` (`GROQ_API_KEY`), with a
local Ollama fallback. No OpenAI is used anywhere in this course.
