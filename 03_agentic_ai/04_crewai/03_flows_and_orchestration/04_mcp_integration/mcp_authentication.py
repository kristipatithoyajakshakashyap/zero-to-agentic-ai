"""MCP AUTHENTICATION: a token-gated MCP server, a client that presents
credentials, and the rejection path when those credentials are missing or wrong.

BEGINNER NOTES
--------------
Every other file in this module quietly assumed the connection was trusted:
the client launched the server, the server handed over every tool it had, and
nobody asked "who are you?". That is fine for a server you launch yourself on
your own machine. It stops being fine the moment the server sits in front of a
real database, a payments API, or another team's data.

So: how do you put a lock on an MCP server?

There are TWO places a credential can be checked, and they answer different
questions. This file shows both, because mixing them up is the classic
beginner mistake.

  1. CONNECTION-LEVEL auth  -> "may this client talk to me at all?"
     The credential is presented ONCE, when the connection is established, and
     covers the whole session. Over stdio the natural carrier is the
     subprocess ENVIRONMENT (the client sets MCP_API_TOKEN when it launches the
     server). Over a network transport the equivalent is an HTTP header —
     `Authorization: Bearer <token>` — which is what MCP's OAuth 2.1 profile
     standardises for streamable-HTTP servers.

  2. CALL-LEVEL auth        -> "may this caller run THIS tool, right now?"
     The credential (or a short-lived session token derived from it) is
     presented with EACH tool call, and the server checks not just that the
     caller is known but that they hold the right SCOPE for that particular
     tool. This is authorisation, not authentication: reading an order and
     refunding an order are the same identity but very different permissions.

Real deployments use both. Connection-level auth stops strangers at the door;
call-level scopes stop a legitimate but low-privilege client from calling the
dangerous tool behind the door.

WHY WE BUILD THE LOCK BY HAND. MCP's specified authorization story (OAuth 2.1,
authorization servers, dynamic client registration) is a network-transport
feature and needs a real identity provider to demonstrate. What that machinery
ultimately produces is exactly what we hand-roll below: a bearer token the
server validates and maps to a set of scopes. Building the small version first
makes the big version legible rather than magic.

SECURITY CAVEAT, stated plainly: the token table in this file is hard-coded
plaintext so the demo is readable. Never do that in production. Real tokens
live in a secret manager, are stored hashed, are scoped narrowly, and expire.

This one file is BOTH the server and the client. Run it with `--server` and it
becomes an MCP stdio server; run it plainly and it launches copies of itself in
server mode and acts as the client.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
(No LLM call is needed for this file — authentication is pure plumbing — but
the resolver is here so every file in the module stays self-contained.)
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from dotenv import load_dotenv

if TYPE_CHECKING:  # `crewai` is imported lazily inside get_llm(), see note there
    from crewai import LLM

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"

# The environment variable the client uses to hand the server its credential
# when launching it over stdio. Over HTTP this would be an Authorization header.
TOKEN_ENV_VAR = "MCP_API_TOKEN"


def _load_track_env() -> None:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> LLM:
    """Resolve an LLM: Groq first, local Ollama fallback. No OpenAI, ever."""
    # Imported here rather than at module top because this same file also runs
    # as the MCP *server* subprocess, which has no business loading CrewAI.
    from crewai import LLM

    _load_track_env()
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kwargs)
        except requests.RequestException:
            pass

    try:
        if requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3).status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kwargs)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


# ---------------------------------------------------------------------------
# THE SERVER SIDE
# ---------------------------------------------------------------------------
# The server's idea of "who exists". In production this is a database lookup
# against HASHED tokens, or a JWT signature check, or a call out to an OAuth
# introspection endpoint. The SHAPE is the same in all three cases: a bearer
# string arrives, and the server turns it into an identity plus a scope set.
#
# Note what a scope is NOT: it is not a role name the client asks for. The
# client sends only the token; the SERVER decides what that token may do. If
# the client could name its own permissions, there would be no security.
KNOWN_TOKENS: dict[str, dict] = {
    "tok_analyst_readonly": {
        "client": "reporting-bot",
        "scopes": {"orders:read"},
    },
    "tok_support_agent": {
        "client": "support-desk",
        "scopes": {"orders:read", "orders:refund"},
    },
}

# A fake order book so the protected tools have something real to return.
ORDERS = {
    "A-100": {"customer": "Ada", "total": 42.50, "status": "delivered"},
    "A-101": {"customer": "Linus", "total": 19.99, "status": "in transit"},
}


def _identify(token: str | None) -> dict | None:
    """Turn a presented bearer token into an identity record, or None.

    Returning None for BOTH "no token" and "unknown token" is deliberate: the
    server must never tell an attacker which of the two it was. Distinguishing
    them in the error message is a real, commonly-shipped information leak.
    """
    if not token:
        return None
    return KNOWN_TOKENS.get(token)


def build_server():
    """Create the FastMCP server whose tools are gated behind a token."""
    from mcp.server.fastmcp import FastMCP

    # ---- 1. CONNECTION-LEVEL CHECK -------------------------------------
    # The client set this environment variable when it launched us. We read it
    # once, at startup, before serving anything. (Over streamable-HTTP the
    # equivalent lives in a middleware that inspects the Authorization header
    # on every request, because an HTTP server serves many clients; a stdio
    # server serves exactly the one process that launched it, so startup is
    # the right moment.)
    presented = os.environ.get(TOKEN_ENV_VAR)
    identity = _identify(presented)

    mcp = FastMCP("course-authenticated-server", log_level="ERROR")

    # If the connection credential is bad we do NOT crash the process. A server
    # that exits on a bad token gives the client an ugly transport error
    # instead of a clean, readable refusal. Instead we come up in a state where
    # every tool refuses — the MCP-friendly way to say 401.
    if identity is None:

        @mcp.tool()
        def whoami() -> str:
            """Report which client the server believes is connected."""
            raise PermissionError(
                "401 Unauthorized: no valid credential was presented on this "
                f"connection. Set the {TOKEN_ENV_VAR} environment variable when "
                "launching the server."
            )

        return mcp

    # ---- Authenticated: register the real tools ------------------------
    @mcp.tool()
    def whoami() -> str:
        """Report which client the server believes is connected, and its scopes."""
        return f"client={identity['client']} scopes={sorted(identity['scopes'])}"

    def _require(scope: str) -> None:
        """Call-level AUTHORISATION check: does this identity hold `scope`?

        Raising an ordinary Python exception is enough — FastMCP catches it and
        returns a proper MCP error result to the client, so the client sees a
        refusal rather than a crashed server.
        """
        if scope not in identity["scopes"]:
            raise PermissionError(
                f"403 Forbidden: client '{identity['client']}' does not hold the "
                f"'{scope}' scope."
            )

    @mcp.tool()
    def get_order(order_id: str) -> str:
        """Look up one order. Requires the 'orders:read' scope."""
        _require("orders:read")
        order = ORDERS.get(order_id)
        if order is None:
            return f"(no such order: {order_id})"
        return f"{order_id}: {order['customer']}, ${order['total']:.2f}, {order['status']}"

    @mcp.tool()
    def refund_order(order_id: str) -> str:
        """Refund one order. Requires the 'orders:refund' scope.

        This is the dangerous tool — it moves money. It deliberately needs a
        STRONGER scope than get_order, which is the whole point of scoping:
        the read-only reporting bot can see this tool in list_tools(), but it
        cannot successfully call it.
        """
        _require("orders:refund")
        order = ORDERS.get(order_id)
        if order is None:
            return f"(no such order: {order_id})"
        return f"Refunded {order_id} (${order['total']:.2f}) for {order['customer']}."

    return mcp


# ---------------------------------------------------------------------------
# THE CLIENT SIDE
# ---------------------------------------------------------------------------
async def _connect_and_probe(token: str | None, label: str) -> None:
    """Launch the server with `token` as its credential, then try both tools.

    Everything interesting happens in the `env=` argument to
    StdioServerParameters — that is the client "presenting credentials".
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import get_default_environment, stdio_client

    # get_default_environment() gives us the minimal safe environment the MCP
    # SDK uses for child processes (PATH, SystemRoot on Windows, and so on).
    # We add our credential on top. Passing the whole of os.environ to a server
    # would leak every other secret on the machine into it — don't.
    child_env = get_default_environment()
    if token is not None:
        child_env[TOKEN_ENV_VAR] = token

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve()), "--server"],
        env=child_env,
    )

    print(f"\n=== {label} ===")
    print(f"  presenting: {token!r}")

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"  tools visible: {[t.name for t in tools.tools]}")

            # `call_tool` does not raise on a server-side error. It returns a
            # result whose `.isError` flag is True and whose content carries
            # the message. Checking that flag IS the rejection path — a client
            # that ignores it will happily treat "403 Forbidden" as an answer.
            for name, args in (
                ("whoami", {}),
                ("get_order", {"order_id": "A-100"}),
                ("refund_order", {"order_id": "A-100"}),
            ):
                if name not in {t.name for t in tools.tools}:
                    print(f"  {name:<13} -> not offered by this server")
                    continue
                result = await session.call_tool(name, args)
                text = result.content[0].text if result.content else "(no content)"
                verdict = "REJECTED" if result.isError else "OK"
                print(f"  {name:<13} -> [{verdict}] {text.strip().splitlines()[-1]}")


async def _run_client() -> None:
    """Three connections, three outcomes: the happy path and two refusals."""
    # 1. A fully-privileged client. Everything works.
    await _connect_and_probe("tok_support_agent", "VALID token, full scopes")

    # 2. A known client with a WEAKER token. It authenticates fine, reads fine,
    #    and is refused on the money-moving tool. Authentication succeeded;
    #    authorisation did not. Beginners routinely conflate these two.
    await _connect_and_probe("tok_analyst_readonly", "VALID token, read-only scope")

    # 3. A token that is not in the table at all. The server comes up in its
    #    refuse-everything state and no tool works.
    await _connect_and_probe("tok_totally_made_up", "WRONG token")

    # 4. No credential presented at all — the same outcome as a wrong one, on
    #    purpose, so an attacker learns nothing from the difference.
    await _connect_and_probe(None, "MISSING credential")

    print(
        "\n--- What to take away ---\n"
        "  * The credential rode on the TRANSPORT (env var here, an\n"
        "    Authorization header over HTTP) - not in the tool arguments,\n"
        "    where the model could see, log, or hallucinate it.\n"
        "  * The SERVER mapped token -> scopes. The client never named its own\n"
        "    permissions.\n"
        "  * A wrong token and a missing token produced identical refusals.\n"
        "  * Refusals came back as normal MCP error results (isError=True),\n"
        "    so a well-written client can handle them instead of crashing.\n"
        "  * The read-only client could SEE refund_order in its tool list and\n"
        "    was still refused when it called it. Scope enforcement lives on\n"
        "    the server, because the model cannot be trusted to enforce it on\n"
        "    itself - hiding a tool is not the same as protecting it."
    )


def demo_authentication() -> None:
    """Sync wrapper so main.py can call this like every other section."""
    asyncio.run(_run_client())
    # A courtesy pause: several subprocesses were just started and stopped.
    time.sleep(0.5)


if __name__ == "__main__":
    if "--server" in sys.argv:
        # Child process: become the MCP server and block, serving over stdio.
        build_server().run(transport="stdio")
    else:
        demo_authentication()
