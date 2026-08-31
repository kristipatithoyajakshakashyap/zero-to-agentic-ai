"""A minimal local MCP server exposed over SSE (Server-Sent Events) transport.

BEGINNER NOTES
--------------
Unlike the stdio server (one process talking to its parent), an SSE server
listens on a real network port, so multiple clients — possibly on
different machines — can connect to it over HTTP. SSE is one of MCP's two
network transports (the other is Streamable HTTP, see mcp_http_server.py).

Run standalone to start listening on http://127.0.0.1:8765/sse.
mcp_http_and_sse_client.py launches this as a background subprocess and
connects to it as a real client (not mocked).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("course-calculator-server", host="127.0.0.1", port=8765)


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="sse")
