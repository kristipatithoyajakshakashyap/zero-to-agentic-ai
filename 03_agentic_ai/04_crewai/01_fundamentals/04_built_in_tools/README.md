# Module 04 - Built-in Tools

> **MLCourse - CrewAI Fundamentals - Built-in Tools**

CrewAI ships with a curated set of tools that agents can use to read files, scrape
websites, search the web, and more. This module catalogs the key built-in tools,
shows how to configure them, and demonstrates them inside a crew.

## What you'll learn

- Use FileReadTool to let agents read local files
- Use ScrapeWebsiteTool to fetch and parse web pages
- Use SerperDevTool for web search powered by Serper
- Configure tool parameters and API keys
- Attach multiple tools to a single agent

## Why this matters

An LLM by itself can only talk - it can't read your files, browse the web, or search
the internet. Tools are what turn a "chatbot" into an "agent" that can actually take
action. Once you attach a tool to an Agent, the LLM decides for itself, mid-task,
when to call it (you never call it manually) - this is the foundation every later
module (custom tools, MCP, multi-agent crews) builds on.

## Key concepts

- **Tool**: a callable that extends what an agent can do
- **Built-in tools**: pre-built integrations shipped with crewai-tools
- **Tool configuration**: API keys, parameters, and defaults
- **Multi-tool agents**: one agent using several tools simultaneously
- **Tool selection**: agents decide which tool to call based on context

## Contents

1. `llm_setup.py` - shared `get_llm()` resolver (Groq, falling back to local Ollama) and `kickoff_with_retry()` helper
2. `file_tools.py` - `FileReadTool` and `FileWriterTool`
3. `directory_tools.py` - `DirectoryReadTool` and `DirectorySearchTool` (semantic search uses a local Ollama embedding model, not OpenAI)
4. `web_scrape_tool.py` - `ScrapeWebsiteTool`
5. `serper_search_tool.py` - `SerperDevTool` (skips cleanly if `SERPER_API_KEY` is unset)
6. `multi_tool_agent.py` - assigning tools to agents, standalone `tool.run()`, defensive error handling, full agent+tools+task+crew pattern
7. `main.py` - Entry point that runs all parts in sequence

LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable. No OpenAI anywhere in this module.

After this module, continue to `05_research_assistant_crew` for the mini-capstone.

## Running

```bash
python main.py
```

Or run any part individually - every file is self-contained and runnable on its own:
```bash
python file_tools.py
python directory_tools.py
python web_scrape_tool.py
python serper_search_tool.py
python multi_tool_agent.py
```
