# Module 04 - MCP Integration

> **MLCourse - Flows and Orchestration - MCP Integration**

Model Context Protocol (MCP) lets CrewAI agents connect to external tool servers.
This module covers MCPServerAdapter, transport protocols, and security
considerations for running MCP servers alongside your crews.

## What you'll learn

- Use MCPServerAdapter to connect to MCP servers
- Understand stdio and SSE transport protocols
- Configure MCP server connections in CrewAI
- Apply security best practices for MCP integration
- Combine MCP tools with CrewAI agents and flows

## Key concepts

- **MCP (Model Context Protocol)**: a standard for connecting LLMs to external tools
- **MCPServerAdapter**: CrewAI's bridge to MCP tool servers
- **stdio transport**: local process communication via stdin/stdout
- **SSE transport**: server-sent events for remote MCP servers
- **Security**: sandboxing, authentication, and permission control

## Contents

1. `01_mcp_basics.ipynb` - MCPServerAdapter setup, connecting to servers
2. `02_transports.ipynb` - stdio vs SSE, when to use each
3. `03_security.ipynb` - sandboxing, auth, permission patterns

After this module, continue to `05_delegation_and_parallel_crews` for multi-crew orchestration.
