# Module 05 - Research Assistant Crew

> **MLCourse - CrewAI Fundamentals - Research Assistant Crew**

The first capstone: build a crew of agents that researches a topic by searching
the web, scraping relevant pages, reading files, and producing a structured report.
This module ties together everything from the Fundamentals category.

## What you'll learn

- Design a multi-agent workflow from scratch
- Assign complementary roles: researcher, writer, reviewer
- Orchestrate tool usage across agents
- Produce structured output from a crew run
- Debug and iterate on crew behavior

## Why this matters

This is the "put it all together" module for Fundamentals: one agent role isn't
very useful on its own, but a researcher + writer + editor chain shows the real
value of CrewAI - specialized agents, each simple on their own, cooperating through
`context=[...]` to produce something none of them could produce alone.

## Key concepts

- **Workflow design**: mapping a real task to agents and tasks
- **Role specialization**: each agent does one thing well
- **Output chaining**: researcher output feeds writer input
- **Quality review**: a reviewer agent critiques the draft
- **End-to-end crew**: complete Agent-Task-Tool-Process pipeline

## Contents

1. `llm_setup.py` - shared `get_llm()` resolver (Groq, falling back to local Ollama) and `kickoff_with_retry()` helper
2. `research_crew.py` - full 3-agent crew (researcher with FileReadTool + ScrapeWebsiteTool, writer, editor), context-chained tasks, saves the final report to disk
3. `basic_variant_no_tools.py` - the same researcher/writer/editor pipeline with no external tools, relying purely on the LLM's own knowledge
4. `main.py` - Entry point that runs both parts in sequence

LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable. No OpenAI anywhere in this module.

After this module, continue to `02_advanced_agents` to extend agents with custom tools, knowledge, and memory.

## Running

```bash
python main.py
```

Or run any part individually - every file is self-contained and runnable on its own:
```bash
python research_crew.py
python basic_variant_no_tools.py
```
