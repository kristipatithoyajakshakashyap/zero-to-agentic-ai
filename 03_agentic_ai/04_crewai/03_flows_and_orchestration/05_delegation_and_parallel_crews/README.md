# 05 — Delegation and Parallel Crews

## What is this, and why does it matter?

Two orchestration patterns that go beyond a single linear crew:

- **Delegation** — an agent decides, on its own, to hand off part of a
  task to a teammate agent better suited for it, instead of a human
  hard-coding "if X then use agent Y" logic.
- **Parallel execution** — running several independent crews at the same
  time instead of one after another, which matters a lot once you have
  multiple sub-tasks that don't depend on each other's results (real time
  savings, since each crew is mostly waiting on LLM API calls).

## Files in this module

| File | What it teaches |
|---|---|
| `delegation_crew.py` | `allow_delegation=True` — a supervisor agent that can hand off work to a specialist teammate. |
| `parallel_crews.py` | `kickoff_async()` + `asyncio.gather()` to run multiple crews concurrently. |
| `fan_out_fan_in_flow.py` | Combines both ideas into a Flow: fan out to N parallel crews, then fan in to one combined summary step. |
| `main.py` | Runs all three files above in sequence. |

## Walkthrough

1. **`delegation_crew.py`** — `allow_delegation=True` on the `Supervisor`
   agent unlocks two built-in tools ("delegate work to co-worker", "ask
   question to co-worker"). The LLM decides at runtime whether to answer
   directly or delegate — there's no explicit routing code to write.

2. **`parallel_crews.py`** — Each topic gets its own tiny one-agent crew.
   `crew.kickoff_async()` returns a coroutine instead of blocking, so
   `asyncio.gather(*coroutines)` runs all of them concurrently and returns
   all results together once every crew is done.

3. **`fan_out_fan_in_flow.py`** — Wraps the parallel pattern in a Flow:
   `fan_out_research` (an `async def` step) kicks off N crews concurrently
   with `asyncio.gather`, then `fan_in_summary` — triggered automatically
   via `@listen` once fan-out completes — combines all results into one
   paragraph. Note that inside a Flow you `await` directly rather than
   calling `asyncio.run()`, since the Flow already runs inside an event loop.

4. **`main.py`** — runs delegation, then parallel crews, then the combined
   fan-out/fan-in flow.

## How to run it

```bash
python delegation_crew.py         # supervisor delegates to a specialist
python parallel_crews.py          # 3 crews running concurrently
python fan_out_fan_in_flow.py     # fan-out to parallel crews, fan-in to a summary
python main.py                    # all three, in sequence
```

Uses your Groq API key from `03_agentic_ai/.env` (`GROQ_API_KEY`), with a
local Ollama fallback. No OpenAI is used anywhere in this course.
