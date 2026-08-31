# Module 07: Travel Planner (Capstone)

> **MLCourse - Agentic AI - Multi-Agent + Human-in-the-Loop**

The LangGraph capstone. One notebook builds a complete travel-planning graph that
chains a research agent, a planning agent, and a human approval gate — putting
every pattern from modules 01-06 to work on a single realistic problem.

## Notebook

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_travel_planner.ipynb](01_travel_planner.ipynb) | The whole project, built in eight phases (below) |

Everything lives in this one notebook by design: the point of a capstone is to
watch the pieces snap together in a single continuous build, rather than to hop
between files.

### The eight phases inside the notebook

1. **State design** - a `TravelState` `TypedDict` carrying `TravelPreferences`,
   `ResearchFindings`, and `TravelPlan` dataclasses plus an `add_messages` channel.
2. **Travel tools** - four `@tool` functions: `search_attractions`,
   `search_hotels`, `search_restaurants`, and `get_weather`. They return canned
   data, so the notebook runs the same way every time and costs nothing.
3. **Research agent** - a node that calls the tools and writes its findings into state.
4. **Planning agent** - a node that turns those findings into a day-by-day itinerary.
5. **Human-in-the-loop approval** - an `approval_gate` node built on `interrupt()`
   and `Command(resume=...)`, so a person signs off before the plan is final.
6. **Complete pipeline** - the `StateGraph` wired
   `START -> research -> plan -> approve -> END`, compiled with a `MemorySaver`
   checkpointer (required for `interrupt()` to be resumable) and drawn as a diagram.
7. **Running the pipeline** - a `run_travel_planner(destination, dates, budget, interests)`
   helper that drives one full request, pausing at the approval gate.
8. **Multi-destination demo** - the same graph run against several trips to show
   that thread-scoped state keeps them cleanly separated.

## Prerequisites

- Module 01 ([Graph Basics](../01_graph_basics/README.md)) - `StateGraph`, nodes, edges
- Module 02 ([Tool-Using Agents](../02_tool_using_agents/README.md)) - `@tool`, agent loops
- Module 03 ([Persistence & Checkpointing](../03_persistence_checkpointing/README.md)) - `MemorySaver`, threads
- Module 04 ([Human-in-the-Loop](../04_human_in_the_loop/README.md)) - `interrupt()` and `Command(resume=...)`
- Module 06 ([Multi-Agent Systems](../06_multi_agent_systems/README.md)) - splitting work across agents

## Model and keys

The notebook uses `ChatOllama` for local, keyless generation. Install Ollama and
pull a model once (see the [track README](../README.md)); no API key is required
to run this module end to end.

## When to use this pattern

- Multi-step workflows where distinct sub-problems deserve their own agent
- Applications where a human must approve output before it is acted on
- Systems combining automated research with constrained planning logic
- Long-running requests that must survive a pause and resume later
