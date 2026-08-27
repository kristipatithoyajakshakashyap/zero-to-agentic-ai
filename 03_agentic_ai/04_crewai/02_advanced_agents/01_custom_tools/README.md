# Module 01 - Custom Tools

> **MLCourse - Advanced Agent Features - Custom Tools**

When built-in tools are not enough, CrewAI lets you create your own. This module
covers the `@tool` decorator for quick tool creation, `BaseTool` subclassing for
full control, and error handling patterns that keep agents resilient.

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

1. `01_tool_decorator.ipynb` - @tool basics, function signatures, return types
2. `02_base_tool_subclass.ipynb` - BaseTool, _run(), args_schema, full control
3. `03_error_handling.ipynb` - try/except, retry patterns, graceful degradation

After this module, continue to `02_knowledge_sources` to give agents domain knowledge.
