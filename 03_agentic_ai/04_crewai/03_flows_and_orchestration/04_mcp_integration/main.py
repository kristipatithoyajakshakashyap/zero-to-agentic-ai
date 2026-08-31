"""Run every section of 04_mcp_integration in sequence.

BEGINNER NOTES
--------------
mcp_stdio_server.py, mcp_sse_server.py, and mcp_http_server.py are servers
meant to be launched BY a client, not run directly — that's why they aren't
imported/called here directly. The two client files below launch them
automatically as subprocesses.

The same is true of mcp_resources.py, mcp_prompts.py and
mcp_full_primitives.py, except those files are their OWN server: run with
`--server` they become an MCP stdio server, and run normally they launch a
copy of themselves and act as the client. Importing their demo function (as
we do here) always gets you the client half.

Order of the tour:
  1. tools      — the primitive you already met (mcp_agent_crew.py)
  2. transports — stdio vs SSE vs streamable-HTTP
  3. resources  — app-controlled read-only context
  4. prompts    — user-controlled, server-owned prompt templates
  5. all three  — one server, one real crew
  6. auth       — putting a lock on the server: tokens, scopes, refusals

PACING: the Groq free tier is roughly 8000 tokens/minute. Sections 1, 4 and 5
each make live LLM calls, so we pause briefly between them rather than firing
them back to back.
"""

from __future__ import annotations

import time

from mcp_agent_crew import run_mcp_agent
from mcp_authentication import demo_authentication
from mcp_full_primitives import demo_full_primitives
from mcp_http_and_sse_client import demo_http, demo_sse
from mcp_prompts import demo_prompts
from mcp_resources import demo_resources

# Seconds to wait between sections that hit the LLM, to stay under the
# Groq free tier's tokens-per-minute budget.
LLM_COOLDOWN_SECONDS = 20


def main() -> None:
    print("=== 1. mcp_agent_crew.py (TOOLS, stdio transport) ===")
    print(run_mcp_agent())
    time.sleep(LLM_COOLDOWN_SECONDS)

    print("\n=== 2. mcp_http_and_sse_client.py (sse + streamable-http transports) ===")
    demo_sse()
    demo_http()

    print("\n=== 3. mcp_resources.py (RESOURCES: app-controlled context) ===")
    demo_resources()  # no LLM call at all — resources are pure plumbing

    print("\n=== 4. mcp_prompts.py (PROMPTS: server-owned templates) ===")
    demo_prompts()
    time.sleep(LLM_COOLDOWN_SECONDS)

    print("\n=== 5. mcp_full_primitives.py (tools + resources + prompts in one crew) ===")
    demo_full_primitives()

    print("\n=== 6. mcp_authentication.py (AUTH: tokens, scopes, rejection paths) ===")
    demo_authentication()  # no LLM call — authentication is pure plumbing


if __name__ == "__main__":
    main()
