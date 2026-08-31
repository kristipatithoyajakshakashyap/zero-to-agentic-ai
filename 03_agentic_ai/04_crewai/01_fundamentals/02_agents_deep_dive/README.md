# Module 02 - Agents Deep Dive

> **MLCourse - CrewAI Fundamentals - Agents Deep Dive**

Every CrewAI agent is defined by three things: a role, a goal, and a backstory.
This module unpacks each parameter, shows how to assign different LLMs to different
agents, and introduces delegation - the mechanism that lets agents hand off work to
each other.

## What you'll learn

- Define agent role, goal, and backstory effectively
- Assign different LLMs to different agents within the same crew
- Enable and control agent delegation
- Use allow_delegation and max_iter parameters
- Write backstories that shape agent behavior

## Key concepts

- **role**: the job title or function the agent performs
- **goal**: the objective the agent strives toward
- **backstory**: narrative context that guides decision-making style
- **LLM assignment**: override the default model per agent
- **delegation**: agents requesting help from other agents in the crew

## Contents

1. `agent_parameters.py` - role/goal/backstory deep dive, all Agent() params, defines the shared `get_llm()` resolver
2. `llm_assignment.py` - different models per agent, all Groq (with local Ollama fallback)
3. `delegation.py` - allow_delegation, when agents ask for help
4. `max_iter.py` - max_iter preventing infinite loops
5. `verbose_reasoning.py` - verbose vs reasoning debugging output
6. `config_approaches.py` - Python constructor, JSON dict, JSON file
7. `main.py` - Entry point that runs all parts in sequence

LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable. No OpenAI anywhere in this module.

After this module, continue to `03_tasks_and_processes` to learn about tasks and execution strategies.

## Beginner walkthrough

- **Why this module exists**: `first_crew.py` in Module 01 hardcoded one
  agent. Here you learn every knob an `Agent` actually has, and how agents
  can be wired to different LLMs or hand work off to each other.
- **`agent_parameters.py`** is the foundation file - it defines `get_llm()`
  and prints a reference table of every `Agent()` parameter (role, goal,
  backstory, llm, tools, allow_delegation, max_iter, verbose, reasoning).
  Every other file in this module imports `llm` from here, so run this one
  first if you're exploring by hand.
- **`llm_assignment.py`** shows you don't have to use one LLM for every
  agent - a "fast" agent and a "deep" agent can point at different models.
- **`delegation.py`** demonstrates `allow_delegation=True`: a manager-style
  agent can ask a specialist agent for help mid-task. This costs extra LLM
  calls (more latency), so only turn it on when agents genuinely need to
  talk to each other.
- **`max_iter.py`** shows `max_iter` as a safety valve - it caps how many
  reasoning loops an agent can take before CrewAI forces it to stop, which
  prevents runaway loops (and runaway API costs).
- **`verbose_reasoning.py`** compares `verbose=True` (prints step-by-step
  thinking) against CrewAI's `reasoning` flag, useful for debugging *why*
  an agent produced a given answer.
- **`config_approaches.py`** shows three equivalent ways to define the same
  agent: plain Python, a dict you `**unpack`, or a JSON file you load at
  runtime - useful once you want agents configured outside your code.

## Running

```bash
python main.py
```

Or run any part individually - every file is self-contained and runnable on its own:
```bash
python agent_parameters.py
python llm_assignment.py
python delegation.py
python max_iter.py
python verbose_reasoning.py
python config_approaches.py
```