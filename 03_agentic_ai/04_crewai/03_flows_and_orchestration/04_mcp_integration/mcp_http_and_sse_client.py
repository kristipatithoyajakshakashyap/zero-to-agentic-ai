"""Launch the SSE and Streamable-HTTP MCP servers as background subprocesses,
connect to each as a real client via crewai_tools.MCPServerAdapter, and use
their tools directly (no agent needed to demonstrate the transports).

BEGINNER NOTES
--------------
This file skips the "Agent" layer on purpose, to keep the focus on the
transport mechanics: start a server process, wait for it to be ready,
connect a client to its URL, call a tool, then shut the server down. Once
you understand this, wiring the same `tools` into an `Agent(tools=...)` is
identical to what mcp_agent_crew.py already does for the stdio transport.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from crewai_tools import MCPServerAdapter

HERE = Path(__file__).resolve().parent


def _start_server(script_name: str, ready_wait_seconds: float = 2.0) -> subprocess.Popen:
    """Start a server script as a background OS process and give it a
    couple seconds to bind its port before we try to connect."""
    proc = subprocess.Popen(
        [sys.executable, str(HERE / script_name)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(ready_wait_seconds)
    return proc


def demo_sse() -> None:
    """Connect to the SSE server by URL — note the dict form of
    MCPServerAdapter's argument, as opposed to StdioServerParameters used
    for the stdio transport in mcp_agent_crew.py."""
    proc = _start_server("mcp_sse_server.py")
    try:
        with MCPServerAdapter({"url": "http://127.0.0.1:8765/sse"}) as tools:
            print(f"[SSE] Tools discovered: {[t.name for t in tools]}")
            add_tool = next(t for t in tools if t.name == "add")
            print("[SSE] add(3, 4) ->", add_tool.run(a=3, b=4))
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def demo_http() -> None:
    proc = _start_server("mcp_http_server.py")
    try:
        with MCPServerAdapter({"url": "http://127.0.0.1:8766/mcp", "transport": "streamable-http"}) as tools:
            print(f"[HTTP] Tools discovered: {[t.name for t in tools]}")
            hour_tool = next(t for t in tools if t.name == "current_utc_hour")
            print("[HTTP] current_utc_hour() ->", hour_tool.run())
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    demo_sse()
    demo_http()
