# Module 05 - Capstone: Full-Stack App Builder

> **MLCourse - Production Readiness - Capstone: Full-Stack App Builder**

## Why this matters

This capstone combines everything from the CrewAI production phase into
one pipeline: six specialist agents (Product Manager, Architect, Frontend
Dev, Backend Dev, QA, Tech Writer) collaborate to turn a plain-text app
specification into user stories, an architecture, code sketches, tests,
and documentation. It's the same shape a real multi-agent product team
would use, just scoped down (short prompts, a simple Todo API spec) so it
runs quickly and cheaply on Groq's free tier.

## What you'll learn

- How to wire six agents into one pipeline, two different ways: sequential
  and Flow-based (with parallel steps and conditional routing)
- Where a human-approval gate belongs in an agentic pipeline, and why
- How to give a crew persistent memory across separate runs
- How to score generated output and check it against a deployment checklist

## Contents

1. **`app_spec.py`** — The sample Todo-API specification (plain data, no LLM calls).
2. **`agents.py`** — Builds all six agents. Creating an `Agent` doesn't call
   the LLM yet — that only happens when a `Task` runs inside a `Crew`.
3. **`tasks.py`** — The six tasks, one per agent, chained with `context=[...]`
   so each agent sees the previous agents' output.
4. **`sequential_crew.py`** — Runs all six agents one after another
   (`Process.sequential`) — the simplest orchestration to understand.
5. **`flow_orchestration.py`** — The same pipeline as a CrewAI `Flow`:
   Frontend and Backend run **in parallel** after the Architect step, then
   a `@router` decides whether QA's result routes to a bug-fix path or
   straight to documentation.
6. **`hitl_gate.py`** — Shows where a human-in-the-loop approval step goes
   (after the Architect, before development). Auto-approves since this
   course runs unattended, but logs exactly what a real approval call
   would look like.
7. **`memory_setup.py`** — Wires up all three CrewAI memory types
   (short-term, long-term/SQLite, entity) on a crew, so agents can
   remember past decisions across separate script runs.
8. **`run_pipeline.py`** — Runs the Flow-based pipeline end to end, saves
   the output to `04_crewai/data/capstone_pipeline_output.txt`, and scores
   it with `metrics.py`.
9. **`metrics.py`** — Simple heuristics for scoring generated text
   (word/line counts, "does it look like code") plus the production
   deployment checklist.
10. **`main.py`** — Runs everything above in order: sequential baseline →
    Flow pipeline + metrics → HITL gate demo → memory setup.

## How to run it

Every file works standalone. If you only run one, run this:

```bash
python run_pipeline.py
```

Or run the whole module:

```bash
python main.py
```

**LLM provider:** Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling
back to local Ollama if Groq is unreachable. Task prompts are kept short
on purpose so the full six-agent pipeline stays well under Groq's free-tier
rate limit.

Congratulations on completing the CrewAI track! You now have the skills to build
production-grade multi-agent systems with role-based agent teams.
