# Module 02: Tool-Using Agents

> **MLCourse - Agentic AI - LangGraph**

Building agents that call external tools — from simple `@tool`-decorated functions to full ReAct loops with `ToolNode`, `tools_condition`, and custom agent graphs.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_tool_integration](01_tool_integration.ipynb) | The `@tool` decorator, tool schemas, and binding tools to an LLM |
| 02 | [02_react_agent_loop](02_react_agent_loop.ipynb) | Constructing a ReAct agent with `ToolNode` and `tools_condition` |
| 03 | [03_multiple_tools](03_multiple_tools.ipynb) | Registering and routing to multiple tools in a single agent |
| 04 | [04_custom_agent_graphs](04_custom_agent_graphs.ipynb) | Building custom agent graphs that go beyond the default ReAct pattern |

## Prerequisites

- Module 01 ([Graph Basics](../01_graph_basics/README.md))

## What you'll learn

- How to define tools using the `@tool` decorator and custom tool classes
- How `ToolNode` executes tools and feeds results back into the graph
- How `tools_condition` decides whether to call a tool or return to the user
- How to build a full ReAct (Reason + Act) loop inside LangGraph
- How to extend or replace the default agent graph with custom logic
