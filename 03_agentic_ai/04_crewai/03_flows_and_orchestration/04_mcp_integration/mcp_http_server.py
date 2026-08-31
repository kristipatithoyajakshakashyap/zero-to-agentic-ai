"""A minimal local MCP server exposed over Streamable HTTP transport.

BEGINNER NOTES
--------------
Streamable HTTP is MCP's newer, recommended network transport — a single
HTTP endpoint that supports both request/response and streaming. It's
generally preferred over SSE for new servers because it's simpler to host
behind standard HTTP infrastructure (load balancers, proxies, etc).

Run standalone to start listening on http://127.0.0.1:8766/mcp.
mcp_http_and_sse_client.py launches this as a background subprocess and
connects to it as a real client (not mocked).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("course-time-server", host="127.0.0.1", port=8766)


@mcp.tool()
def current_utc_hour() -> int:
    """Return the current UTC hour (0-23)."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).hour


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
