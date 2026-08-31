# Module 04 - Reasoning and Planning

> **MLCourse - Advanced Agent Features - Reasoning and Planning**

CrewAI agents can reason through problems step by step and plan their approach
before executing. This module covers chain-of-thought prompting, crew-level
planning, and strategies for making agents think before they act.

## What you'll learn

- Enable chain-of-thought reasoning in agents
- Use crew planning to decompose complex tasks
- Configure reasoning parameters and depth
- Balance reasoning quality with speed and cost
- Debug reasoning chains to understand agent decisions

## Key concepts

- **Chain-of-thought**: step-by-step reasoning before answering
- **Crew planning**: the crew plans task execution before acting
- **Reasoning depth**: controlling how much thinking happens
- **Think tag**: internal reasoning that does not appear in final output
- **Planning agents**: agents that orchestrate other agents' work

## Beginner walkthrough

Two different "thinking" features, easy to mix up:
- **Agent reasoning** (`agent_reasoning.py`) is one agent thinking through
  its OWN task before answering — like a student showing their work on a
  single math problem. Turn it on with `reasoning=True` on the `Agent`.
- **Crew planning** (`crew_planning.py`) happens BEFORE any agent starts
  working — the crew looks at the whole task list and adds guidance to
  each task first, like a project manager sketching a plan before the team
  begins. Turn it on with `planning=True` on the `Crew`.
- `reasoning_plus_planning.py` uses both at once and explains when you'd
  want each — reasoning for individual hard tasks, planning for
  multi-step crews.
- `main.py` runs the whole module in order.

Run any file on its own with `python <filename>.py`, or the whole module
with `python main.py`.

## Contents

1. `agent_reasoning.py` - agent-level reasoning=True, step-by-step thinking
2. `crew_planning.py` - crew-level planning=True, task decomposition
3. `reasoning_plus_planning.py` - combining both, when to use each
4. `main.py` - runs every section above in sequence

Every file runs standalone (`python <file>.py`); `main.py` runs the whole module.
Uses Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`) with local Ollama as fallback.

After this module, continue to `05_conditional_and_multimodal` for advanced task types.
