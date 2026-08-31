"""MCP RESOURCES: an MCP server that exposes readable *context*, plus a client
that lists and reads it.

BEGINNER NOTES
--------------
MCP has THREE primitives, not one. The rest of this module only showed the
first:

  1. TOOLS      - MODEL-controlled. The LLM decides to call them. They DO
                  something (send an email, run a query, reverse a string).
  2. RESOURCES  - APPLICATION-controlled. Read-only data identified by a URI,
                  like files in a filesystem. *Your code* decides which ones
                  to read and paste into the prompt. The model never "calls"
                  a resource.
  3. PROMPTS    - USER-controlled prompt templates (see mcp_prompts.py).

The single most important difference: a tool is a VERB with side effects that
the model invokes; a resource is a NOUN — an addressable, read-only blob of
context that the app fetches. If you find yourself writing a tool called
`get_config()` that takes no arguments and just returns text, that should
almost certainly have been a resource instead.

Resources come in two flavours, both shown below:
  * static resources    - a fixed URI, e.g. "course://policies/refunds"
  * resource templates  - a URI with {placeholders}, e.g.
                          "course://students/{student_id}", so one handler can
                          serve a whole family of addresses.

WHY NOT MCPServerAdapter HERE? `crewai_tools.MCPServerAdapter` deliberately
surfaces only TOOLS, because that is the only primitive a CrewAI `Agent` can
call by itself. Resources are app-controlled, so we talk to the server with
the official `mcp` SDK's raw `ClientSession` instead — that's the layer where
list_resources()/read_resource() live.

This one file is BOTH the server and the client. Run it with `--server` and
it becomes an MCP stdio server; run it plainly and it launches a copy of
itself in server mode and acts as the client.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
(No LLM call is actually needed for this file — reading resources is pure
plumbing — but the resolver is here so every file stays self-contained.)
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from dotenv import load_dotenv

if TYPE_CHECKING:  # `crewai` is imported lazily inside get_llm(), see note there
    from crewai import LLM

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


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
# A tiny fake "company handbook" the server will serve as resources. In a real
# server these would come from a database, a git repo, S3, a wiki, etc.
POLICIES = {
    "refunds": "Refunds are issued within 14 days of purchase, no questions asked.",
    "shipping": "Standard shipping is 3-5 business days. Express is next-day.",
}

STUDENTS = {
    "s-001": {"name": "Ada", "track": "Agentic AI", "progress_pct": 72},
    "s-002": {"name": "Linus", "track": "Classical ML", "progress_pct": 41},
}


def build_server():
    """Create the FastMCP server that exposes resources (and zero tools)."""
    from mcp.server.fastmcp import FastMCP

    # log_level="ERROR" keeps the server's per-request INFO chatter out of the
    # terminal; the client and server share this console.
    mcp = FastMCP("course-handbook-resources", log_level="ERROR")

    # --- STATIC RESOURCE -------------------------------------------------
    # @mcp.resource() takes a URI. The scheme ("course://") is yours to
    # invent — MCP does not care, it's just an identifier namespace. The
    # function body runs when a client calls read_resource() on that URI.
    @mcp.resource("course://handbook/index", mime_type="text/plain")
    def handbook_index() -> str:
        """A plain-text listing of every policy topic available."""
        return "Available policy topics:\n" + "\n".join(f"- {k}" for k in POLICIES)

    # --- RESOURCE TEMPLATE ----------------------------------------------
    # A {placeholder} in the URI turns this into a *template*: the client can
    # read course://handbook/policies/refunds or .../shipping, and the piece
    # matched by {topic} arrives as the function argument. One handler,
    # infinitely many addresses.
    @mcp.resource("course://handbook/policies/{topic}", mime_type="text/plain")
    def policy(topic: str) -> str:
        """Return the text of one company policy by topic name."""
        return POLICIES.get(topic, f"(no policy found for topic '{topic}')")

    # Resources are not limited to plain text — declare a mime_type and
    # return whatever string encodes it. JSON is very common.
    @mcp.resource("course://students/{student_id}", mime_type="application/json")
    def student_record(student_id: str) -> str:
        """Return one student's record as JSON."""
        return json.dumps(STUDENTS.get(student_id, {"error": f"unknown student {student_id}"}))

    return mcp


# ---------------------------------------------------------------------------
# THE CLIENT SIDE
# ---------------------------------------------------------------------------
async def _run_client() -> None:
    """Launch this file in --server mode and inspect its resources.

    The three calls that matter, and their tool-side equivalents:

        list_resources()           <-> list_tools()
        list_resource_templates()  <-> (no tool equivalent)
        read_resource(uri)         <-> call_tool(name, args)
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve()), "--server"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # Every MCP session starts with a handshake. The adapter did this
            # for us in mcp_agent_crew.py; at this raw layer we do it ourselves.
            await session.initialize()

            # Notice: the server exposes NO tools at all. Resources are a
            # completely separate namespace from tools.
            tools = await session.list_tools()
            print(f"Tools on this server: {[t.name for t in tools.tools]}  <- intentionally empty")

            listed = await session.list_resources()
            print("\nStatic resources:")
            for res in listed.resources:
                print(f"  {res.uri}  (mime={res.mimeType})  {res.description or ''}")

            templates = await session.list_resource_templates()
            print("\nResource templates (fill in the {placeholder} to address one):")
            for tpl in templates.resourceTemplates:
                print(f"  {tpl.uriTemplate}  (mime={tpl.mimeType})  {tpl.description or ''}")

            # Now actually READ resources. read_resource returns a result with
            # a `.contents` list, because one URI may yield several blobs.
            print("\n--- Reading resources ---")
            for uri in (
                "course://handbook/index",
                "course://handbook/policies/refunds",
                "course://students/s-001",
            ):
                result = await session.read_resource(uri)
                for content in result.contents:
                    print(f"\n[{uri}]\n{content.text}")

            # THE PAYOFF: because resources are app-controlled, *you* choose
            # what lands in the prompt. This is exactly how you would build a
            # context block to hand to an agent — no LLM decision involved.
            refunds = (await session.read_resource("course://handbook/policies/refunds")).contents[0].text
            shipping = (await session.read_resource("course://handbook/policies/shipping")).contents[0].text
            context_block = f"COMPANY POLICIES\n- Refunds: {refunds}\n- Shipping: {shipping}"
            print("\n--- Context block assembled by the APP (not the model) ---")
            print(context_block)


def demo_resources() -> None:
    """Sync wrapper so main.py can call this like every other section."""
    asyncio.run(_run_client())


if __name__ == "__main__":
    if "--server" in sys.argv:
        # Child process: become the MCP server and block, serving over stdio.
        build_server().run(transport="stdio")
    else:
        demo_resources()
