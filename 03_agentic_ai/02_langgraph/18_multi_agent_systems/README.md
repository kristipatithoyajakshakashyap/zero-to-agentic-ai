# Module 18: Multi-Agent Systems

> **MLCourse - Agentic AI - LangGraph**

Composing multiple agents into coordinated systems — supervisor orchestration, swarm-style handoffs, hierarchical agent teams, and parallel agent execution.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_supervisor_pattern](01_supervisor_pattern.ipynb) | A supervisor agent that routes tasks to specialized worker agents |
| 02 | [02_swarm_handoff](02_swarm_handoff.ipynb) | Agents that dynamically hand off control to each other based on context |
| 03 | [03_hierarchical_supervisors](03_hierarchical_supervisors.ipynb) | Nesting supervisors to form hierarchical agent organizations |
| 04 | [04_parallel_agents](04_parallel_agents.ipynb) | Running multiple agents concurrently and aggregating their results |

## Prerequisites

- Module 14 (Tool-Using Agents)
- Module 17 (Streaming)

## What you'll learn

- How to design a supervisor that delegates tasks to the right agent
- How swarm-style handoffs let agents pass control without a central coordinator
- How to build hierarchical teams with nested supervisor graphs
- How to run agents in parallel and merge their outputs for faster workflows
