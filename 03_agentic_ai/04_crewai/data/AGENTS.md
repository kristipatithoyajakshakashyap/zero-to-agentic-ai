# AGENTS.md -- Project Configuration for Coding Agents

## Project Overview
Demo project showing how coding agents interact with CrewAI.

## Directory Structure
- src/ : Application source code
- tests/ : Unit and integration tests
- data/ : Training and input data files

## Coding Conventions
- Python 3.11+ with type hints
- PEP 8 style
- All public functions must have docstrings

## Available Tools
- RunPython: Execute Python code in a sandboxed subprocess
- FileReadTool: Read file contents
- SerperDevTool: Web search (requires SERPER_API_KEY)

## Safety Rules
- Never execute code that modifies system files
- Always validate inputs before processing
- Use try/except for all external calls
