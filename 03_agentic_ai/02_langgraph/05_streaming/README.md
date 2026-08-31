# Module 05: Streaming

> **MLCourse - Agentic AI - LangGraph**

Real-time output from graphs — token-level streaming with `stream()` and `astream_events`, handling multi-node workflows, and delivering responsive user experiences.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_stream_basics](01_stream_basics.ipynb) | `stream()` vs `invoke()` — streaming node outputs as they complete |
| 02 | [02_token_streaming](02_token_streaming.ipynb) | Token-level streaming with `astream_events` and LLM streaming callbacks |
| 03 | [03_streaming_multi_node](03_streaming_multi_node.ipynb) | Streaming across complex multi-node graphs with parallel branches |

## Prerequisites

- Module 02 ([Tool-Using Agents](../02_tool_using_agents/README.md))

## What you'll learn

- The difference between `stream()`, `astream()`, and `astream_events()`
- How to stream individual tokens from an LLM call inside a graph node
- How to handle streaming across multiple nodes and conditional branches
- How to build responsive UIs that display agent output in real time
