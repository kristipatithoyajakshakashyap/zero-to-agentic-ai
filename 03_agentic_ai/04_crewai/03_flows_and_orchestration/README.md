# Flows and Orchestration

CrewAI Flows bring typed state, persistence, human-in-the-loop gates, and MCP
integration to multi-agent workflows. Orchestrate multiple crews in parallel or
chain them through delegation pipelines.

## Modules

| Folder | Teaches |
|---|---|
| [01_flows_basics](./01_flows_basics/README.md) | Flow class, @start, @listen, typed state |
| [02_flow_state_persistence](./02_flow_state_persistence/README.md) | @persist, SQLite checkpointing, resume/fork |
| [03_human_in_the_loop](./03_human_in_the_loop/README.md) | @human_feedback, approval gates |
| [04_mcp_integration](./04_mcp_integration/README.md) | MCPServerAdapter, transports, security |
| [05_delegation_and_parallel_crews](./05_delegation_and_parallel_crews/README.md) | Delegation chains, parallel crews |

## Prerequisites

Complete the **CrewAI Fundamentals** and **Advanced Agent Features** categories.
Familiarity with agents, tasks, and CrewAI's API is assumed.
