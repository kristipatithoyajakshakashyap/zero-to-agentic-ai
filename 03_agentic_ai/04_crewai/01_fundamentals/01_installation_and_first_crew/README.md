# Module 01 - Installation and First Crew

> **MLCourse - CrewAI Fundamentals - Installation and First Crew**

Get CrewAI running on your machine and build your first multi-agent crew from
scratch. This module covers installation, CLI scaffolding, and the minimal
Agent-Task-Crew triangle that every CrewAI application is built from.

## What you'll learn

- Install CrewAI and its optional tooling extras with pip
- Scaffold a new CrewAI project using the CLI
- Define agents with role, goal, and backstory
- Wire agents to tasks and run a crew end-to-end
- Understand the Agent-Task-Crew relationship

## Key concepts

- **Agent**: an autonomous unit with a role, goal, backstory, and optional LLM
- **Task**: a unit of work assigned to an agent with a description and expected output
- **Crew**: a team of agents executing a sequence of tasks
- **Process**: the execution strategy (sequential by default)
- **kickoff()**: the entry point that runs the crew

## Contents

1. `install_check.py` - pip install walkthrough, version check, verification
2. `cli_scaffolding.py` - crewai create crew, project structure, run
3. `first_crew.py` - minimal Agent-Task-Crew triangle (Groq-backed LLM, with local Ollama fallback), kickoff, output
4. `main.py` - Entry point that runs all parts in sequence

## Beginner walkthrough

New to CrewAI? Read this before running anything.

- **Why this module exists**: before you can build multi-agent systems, you
  need CrewAI installed correctly and a mental model of its three core
  building blocks - Agent, Task, Crew. Everything later in this course is
  built on top of this triangle.
- **`install_check.py`** confirms CrewAI (and the extra tools package) is
  actually importable in your environment. Run this first if anything else
  in the course fails with an `ImportError`.
- **`cli_scaffolding.py`** is documentation-as-code: it prints out the
  `crewai create crew` / `crewai run` / `crewai test` commands and what
  project structure they generate. It doesn't build anything itself - it's
  a reference you can re-run any time you forget a CLI command.
- **`first_crew.py`** is the important one. It builds the smallest possible
  working crew: one `Agent` (a "Greeter") given one `Task` (say hello),
  wired into one `Crew`, then run with `crew.kickoff()`. Watch the console
  output - `verbose=True` prints the agent's internal reasoning so you can
  see the LLM call happen live. The `get_llm()` function at the top of the
  file is what picks Groq (or Ollama as backup) - every later module reuses
  this same pattern.
- **`main.py`** just calls the three files above in order, so you can see
  the whole module run start to finish with one command.

LLM provider: this course runs on **Groq** (set `GROQ_API_KEY` in `03_agentic_ai/.env`). If Groq is unreachable, scripts fall back to a local Ollama server. OpenAI is never used.

After this module, continue to `02_agents_deep_dive` to understand agents in depth.

## Running

```bash
python main.py
```

Or run any part individually - every file is self-contained and runnable on its own:
```bash
python install_check.py
python cli_scaffolding.py
python first_crew.py
```