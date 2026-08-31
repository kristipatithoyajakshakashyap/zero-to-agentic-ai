# 01 — Flows Basics

## What is a Flow, and why does it matter?

A **Crew** runs one group of agents on one set of tasks. A **Flow** is a
level above that: it lets you chain multiple steps — each step can be its
own crew, or plain Python — into a pipeline, where the output of one step
automatically becomes the input of the next.

Why this matters: real applications rarely need just "one crew, one
answer." You usually need *research, then write, then review*, or *plan,
then execute, then check*. Flows give you a clean, declarative way to wire
those steps together instead of manually calling crews in order and
passing data between them by hand.

## Files in this module

| File | What it teaches |
|---|---|
| `flow_state.py` | Defines a typed "shared notebook" (`ResearchFlowState`) that every step of the flow can read and write. |
| `research_write_review_flow.py` | The actual 3-step Flow: a Researcher agent gathers notes, a Writer agent turns them into a paragraph, a Reviewer agent gives feedback — each step automatically triggered by the previous one finishing. |
| `main.py` | Runs both files above in order, so you can see the whole module in one command. |

## Walkthrough

1. **`flow_state.py`** — Before you can chain steps together, you need a
   place to store what each step produces. `ResearchFlowState` is a
   Pydantic model with four fields (`topic`, `research_notes`, `draft`,
   `review_notes`), each starting empty and filled in as the flow runs.

2. **`research_write_review_flow.py`** — `ResearchWriteReviewFlow` is a
   Python class that subclasses CrewAI's `Flow`. Look for two decorators:
   - `@start()` marks `research()` as the entry point — it runs first.
   - `@listen(research)` marks `write()` as a method that runs
     automatically once `research()` finishes, receiving its return value.
   - `@listen(write)` does the same for `review()`.

   Each of the three methods builds one `Agent`, gives it one `Task`, runs
   a single-agent `Crew`, and stores the result on `self.state`. This keeps
   each step small and easy to follow.

3. **`main.py`** — calls the state demo and then runs the full flow,
   printing the research notes, the draft, and the review feedback.

## How to run it

From inside this folder:

```bash
python flow_state.py                    # just the state model
python research_write_review_flow.py    # the full 3-step flow
python main.py                          # both, in sequence
```

Uses your Groq API key from `03_agentic_ai/.env` (`GROQ_API_KEY`). If Groq
isn't reachable, it automatically falls back to a local Ollama model
(`ollama pull llama3.1:8b`) — no OpenAI is used anywhere in this course.
