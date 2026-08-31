# Module 01: Graph Basics

> **MLCourse - Agentic AI - LangGraph**

Introduction to LangGraph fundamentals — why graphs matter for agentic AI, and how to build, connect, and control nodes using `StateGraph`, edges, conditional routing, and state reducers.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_langgraph](01_why_langgraph.ipynb) | Motivation for LangGraph over plain chains — graphs as a mental model for agent workflows |
| 02 | [02_state_nodes_edges](02_state_nodes_edges.ipynb) | Defining `TypedDict` state, adding nodes, and connecting them with edges |
| 03 | [03_conditional_routing](03_conditional_routing.ipynb) | Using functions as edge conditions to branch execution dynamically |
| 04 | [04_state_reducers](04_state_reducers.ipynb) | Managing state updates with `Annotated` reducers (`add`, `operator.add`, custom reducers) |

## Prerequisites

- The [01_langchain](../../01_langchain/README.md) track (chat models, prompts, LCEL) - LangGraph assumes you can already build a simple chain

## What you'll learn

- Why a graph-based abstraction is better than linear chains for agentic workflows
- How to define typed state with `TypedDict` and annotate it with reducers
- How to create nodes (functions) and wire them together with edges
- How to use conditional edges to route execution based on runtime state
- How state reducers control how updates are merged across node invocations
