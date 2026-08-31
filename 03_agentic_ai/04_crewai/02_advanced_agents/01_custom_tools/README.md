# Module 01 - Custom Tools

> **MLCourse - Advanced Agent Features - Custom Tools**

When built-in tools are not enough, CrewAI lets you create your own. This module
covers the `@tool` decorator for quick tool creation, `BaseTool` subclassing for
full control, and error handling patterns that keep agents resilient.

**Why this matters:** an agent is only as useful as what it can *do*. Built-in
tools (file reading, web scraping, search) cover common cases, but real
projects almost always need one or two tools specific to your own app —
calling your own API, running a calculation, checking a business rule. This
module teaches the two ways to build those: a quick one-line decorator for
simple functions, and a full class for tools that need validated inputs.

## What you'll learn

- Create tools with the `@tool` decorator
- Build reusable tools by subclassing BaseTool
- Add input validation and error handling
- Register custom tools with agents
- Test tools independently before wiring them into crews

## Key concepts

- **@tool decorator**: turn any function into a CrewAI tool in one line
- **BaseTool subclass**: full control over name, description, _run(), args_schema
- **Error handling**: graceful failures that don't crash the crew
- **Input validation**: Pydantic models for tool arguments
- **Tool testing**: running tools in isolation

## Contents

1. `tool_decorator_basics.py` - @tool basics, function signatures, return types
2. `base_tool_subclass.py` - BaseTool, _run(), args_schema, full control
3. `tool_error_handling.py` - try/except, retry patterns, graceful degradation
4. `tool_hooks.py` - pre/post call hooks around tool execution
5. `agent_with_custom_tools.py` - wiring a custom tool into a real agent + crew
6. `main.py` - runs every section above in sequence

Every file runs standalone (`python <file>.py`); `main.py` runs the whole module.
Uses Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`) with local Ollama as fallback.

After this module, continue to `02_knowledge_sources` to give agents domain knowledge.
