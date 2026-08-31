"""A minimal local MCP server, run over stdio, exposing one tool.

BEGINNER NOTES
--------------
MCP (Model Context Protocol) is an open standard for exposing tools to AI
agents over a stable interface, so a tool provider and an agent framework
don't need to know anything about each other's internals — the agent just
speaks MCP. "stdio transport" means the client (mcp_agent_crew.py) starts
this script as a subprocess and talks to it by writing/reading its
standard input/output streams — no network port needed at all.

This is a real, runnable MCP server (using the official `mcp` SDK's
FastMCP helper) — not a mock. mcp_agent_crew.py launches this file as a
subprocess and talks to it over stdio via crewai_tools.MCPServerAdapter.

NOTE: running `python mcp_stdio_server.py` directly from a terminal will
sit and wait for a client to connect over stdin — that's expected. Use
mcp_agent_crew.py (or main.py) to see it in action.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

# FastMCP is a decorator-based helper: every @mcp.tool()-decorated function
# below automatically becomes a tool the connecting agent can discover and call.
mcp = FastMCP("course-word-count-server")


@mcp.tool()
def word_count(text: str) -> int:
    """Count the number of whitespace-separated words in `text`."""
    return len(text.split())


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the given string."""
    return text[::-1]


if __name__ == "__main__":
    # This call blocks forever, listening for a client over stdio.
    mcp.run(transport="stdio")
