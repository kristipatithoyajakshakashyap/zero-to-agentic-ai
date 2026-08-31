# Module 03 - Coding Agents and CLI

> **MLCourse - Production Readiness - Coding Agents and CLI**

## Why this matters

Sometimes the best way for an AI agent to answer a question is to actually
run code and see what happens, instead of guessing the answer from
pattern-matching. A "coding agent" is just a normal CrewAI agent that has
been given a tool for executing Python. This module also covers the two
things every real CrewAI project needs on the command line: the `crewai`
CLI (for scaffolding and running projects) and the `AGENTS.md` file
(instructions that tell any AI coding assistant working on your repo how
it's organized).

## What you'll learn

- How to give an agent a tool that runs Python code safely, and get the result back
- What `AGENTS.md` is for and why AI coding tools look for it
- The `crewai create crew` / `crewai run` / `crewai test` CLI commands
- How to make an agent retry when its generated code fails

## Contents

1. **`code_interpreter_agent.py`** — Walks through: writing `AGENTS.md`,
   building a `RunPython` tool (a `@tool`-decorated function that runs
   Python in a subprocess and returns the output — this avoids needing
   Docker, which CrewAI's built-in `CodeInterpreterTool` normally
   requires), a validate-and-retry pattern for code that might fail, and
   finally a real Groq-powered agent that writes and runs a Fibonacci
   script.
2. **`cli_reference.py`** — Prints the live output of `crewai --help` and
   `crewai run --help` from the CLI actually installed in this
   environment, shows what a scaffolded project (`crewai create crew`)
   looks like, and lists the CLI commands you'll use day to day.
3. **`main.py`** — Runs both files above in order.

## How to run it

Each file works standalone:

```bash
python code_interpreter_agent.py
python cli_reference.py
python main.py   # runs everything in one go
```

**LLM provider:** Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling
back to local Ollama if Groq is unreachable. This module uses the
`qwen/qwen3.8-27b` Groq model, which is the default across this whole
course phase (Groq's `openai/gpt-oss-*` models are avoided even though
Groq-hosted, since the "openai/" name is confusing in a Groq-only course,
and they also have a tool-calling bug that crashes coding-agent runs).

After this module, continue to `04_llm_connections` for provider configuration.
