# Module 03 - Tasks and Processes

> **MLCourse - CrewAI Fundamentals - Tasks and Processes**

Tasks are the units of work agents execute. This module covers task description,
expected output, agent assignment, context passing between tasks, and the two
process strategies: sequential (linear handoff) and hierarchical (manager agent
delegates).

## What you'll learn

- Define tasks with description, expected output, and agent assignment
- Pass context between sequential tasks
- Choose between sequential and hierarchical processes
- Kick off crews asynchronously
- Use the manager agent pattern effectively

## Key concepts

- **Task**: work unit with description, expected_output, and agent
- **context**: prior task outputs available to the current task
- **sequential process**: tasks run in order, each receiving prior outputs
- **hierarchical process**: a manager agent delegates to worker agents
- **async kickoff**: kick_off_async() for non-blocking execution

## Contents

1. `task_basics.py` - Task() parameters: description, expected_output, agent, callback, output_file, output_pydantic, output_json (defines the shared `get_llm()` resolver)
2. `sequential_hierarchical.py` - Process.sequential (planner -> writer -> editor chain) vs Process.hierarchical (manager_llm delegates to workers)
3. `context_passing.py` - passing a prior task's output into a later task via `context=[...]`
4. `callbacks.py` - `Task(callback=...)` to react to a task finishing
5. `output_parsing.py` - reading `CrewOutput.raw`, `.pydantic`, `.json_dict`, `.token_usage`
6. `async_kickoff.py` - `await crew.kickoff_async()` for non-blocking execution
7. `batch_kickoff_for_each.py` - `crew.kickoff_for_each()` to run the same crew over a batch of inputs
8. `main.py` - Entry point that runs all parts in sequence

LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable. No OpenAI anywhere in this module.

After this module, continue to `04_built_in_tools` to learn about CrewAI's tool catalog.

## Beginner walkthrough

- **Why this module exists**: Module 02 was all about agents. Now it's time
  to understand the *work* agents do - `Task` objects - and the different
  ways a `Crew` can schedule that work.
- **`task_basics.py`** is the foundation file - it walks through every
  `Task()` parameter and defines `get_llm()`, which every other file in
  this module imports.
- **`sequential_hierarchical.py`** is the key concept file: **sequential**
  process runs tasks strictly in list order (each task can see what came
  before it); **hierarchical** process adds a manager agent that plans and
  delegates tasks to worker agents dynamically - more flexible, more LLM
  calls, and it requires you to pass a `manager_llm`.
- **`context_passing.py`** shows how a "research" task's output becomes an
  input to a "summarize" task by putting `context=[research_task]` on the
  second `Task` - this is how information flows between steps.
- **`callbacks.py`** shows attaching a Python function to `Task(callback=...)`
  so you can log, save, or react the moment a task finishes - handy for
  progress bars or writing intermediate results to disk.
- **`output_parsing.py`** shows what you actually get back from
  `crew.kickoff()`: a `CrewOutput` object with `.raw` text, optional
  `.pydantic`/`.json_dict` if you set structured output, and `.token_usage`
  for cost tracking.
- **`async_kickoff.py`** and **`batch_kickoff_for_each.py`** cover running
  crews without blocking your program, and running the *same* crew over
  many different inputs (e.g. summarizing 10 articles) in one call.
