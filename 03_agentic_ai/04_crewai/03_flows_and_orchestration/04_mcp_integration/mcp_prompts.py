"""MCP PROMPTS: an MCP server that ships reusable PROMPT TEMPLATES, plus a
client that lists them, fills them in, and feeds the result to a real LLM.

BEGINNER NOTES
--------------
The third MCP primitive (after tools in mcp_agent_crew.py and resources in
mcp_resources.py) is the PROMPT.

An MCP prompt is a named, argument-taking template that lives ON THE SERVER.
The client asks "what prompts do you offer?", picks one, passes arguments,
and gets back a ready-to-send list of chat messages.

  tools     -> MODEL-controlled  ("the LLM decided to call this")
  resources -> APP-controlled    ("my code decided to read this")
  prompts   -> USER-controlled   ("the human picked this from a menu")

That last one is why MCP clients like Claude Desktop show server prompts as
slash-commands: they are meant to be *chosen*, not auto-invoked.

WHEN IS A SERVER-PROVIDED PROMPT BETTER THAN HARD-CODING ONE CLIENT-SIDE?

  1. The prompt and the data belong together. Whoever wrote the incident
     database knows how to phrase a good incident summary. Shipping the
     wording next to the tools/resources keeps expertise in one place.
  2. You can improve it without redeploying every client. Fix a weak
     instruction on the server and every agent that connects picks it up on
     its next handshake. A prompt baked into your app is a code release.
  3. One template, many consumers. Three teams' agents all summarising
     incidents the same way is a consistency win you cannot get by
     copy-pasting f-strings into three repos.
  4. The server can compose the prompt from live data — the template body is
     real Python, so it can inline the current runbook, today's thresholds,
     or the caller's tier, none of which the client knows.

  Conversely, KEEP IT CLIENT-SIDE when the wording is specific to your one
  app's UX, changes with your own release cycle, or contains details the
  server has no business knowing.

WHY NOT MCPServerAdapter HERE? `crewai_tools.MCPServerAdapter` surfaces only
TOOLS, since that's the only primitive an `Agent` can invoke on its own. To
reach prompts we drop to the official `mcp` SDK's `ClientSession`, which is
where list_prompts()/get_prompt() live.

This one file is BOTH the server and the client: run it with `--server` and
it becomes an MCP stdio server; run it plainly and it launches a copy of
itself in server mode and acts as the client.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base  # module-level so FastMCP can resolve
                                             # the `list[base.Message]` annotation below

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
# Pretend this lives inside the incident-management team's MCP server, next to
# their incident database. They own the wording; consumers just fill blanks.
SEVERITY_RUNBOOK = {
    "sev1": "Page the on-call lead immediately and open a war room.",
    "sev2": "Notify the owning team in #incidents within 15 minutes.",
    "sev3": "File a ticket; handle during business hours.",
}


def build_server():
    """Create the FastMCP server that exposes prompt templates (and no tools)."""
    mcp = FastMCP("course-incident-prompts", log_level="ERROR")

    # --- SIMPLEST FORM: return a string --------------------------------
    # Returning a plain string is shorthand for "one user message with this
    # text". The function's parameters become the prompt's declared arguments,
    # and the docstring becomes its description in the client's menu.
    @mcp.prompt()
    def summarize_incident(report: str, audience: str = "engineers") -> str:
        """Summarize a raw incident report for a specific audience."""
        return (
            f"Summarize the incident report below for an audience of {audience}.\n"
            "Use exactly three bullets: what broke, blast radius, next action.\n"
            "Keep each bullet under 20 words.\n\n"
            f"REPORT:\n{report}"
        )

    # --- STRUCTURED FORM: return a list of messages ---------------------
    # Real prompts are often multi-turn: a role-setting assistant message, a
    # worked example, then the actual question. Return base.UserMessage /
    # base.AssistantMessage objects to control the shape precisely.
    #
    # Note this template INLINES server-side knowledge (SEVERITY_RUNBOOK) that
    # the client does not have. That is the "server composes from live data"
    # argument for server-provided prompts, made concrete.
    @mcp.prompt()
    def triage_alert(alert_text: str, severity: str = "sev2") -> list[base.Message]:
        """Triage an alert, applying this org's severity runbook."""
        runbook = SEVERITY_RUNBOOK.get(severity, SEVERITY_RUNBOOK["sev3"])
        return [
            base.AssistantMessage(
                "I am this organization's incident triage assistant. "
                f"For {severity} the runbook says: {runbook}"
            ),
            base.UserMessage(
                f"Triage this alert and state the single required next action.\n\n{alert_text}"
            ),
        ]

    return mcp


# ---------------------------------------------------------------------------
# THE CLIENT SIDE
# ---------------------------------------------------------------------------
def _to_chat_messages(prompt_result) -> list[dict]:
    """Convert an MCP GetPromptResult into the plain [{'role','content'}]
    list that essentially every LLM API (including CrewAI's `LLM.call`)
    expects. This little adapter is the whole integration.

    MCP message roles are only 'user' and 'assistant'; content is a typed
    block, and for text prompts it's a TextContent with a `.text` field.
    """
    messages: list[dict] = []
    for msg in prompt_result.messages:
        text = getattr(msg.content, "text", str(msg.content))
        messages.append({"role": msg.role, "content": text})
    return messages


async def _run_client(call_llm: bool = True) -> None:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve()), "--server"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1) DISCOVER. This is the "menu" a UI would render as slash
            #    commands. Each prompt advertises its arguments, so the client
            #    knows what blanks the user has to fill.
            listed = await session.list_prompts()
            print("Prompts offered by the server:")
            for p in listed.prompts:
                args = ", ".join(
                    f"{a.name}{'' if a.required else '?'}" for a in (p.arguments or [])
                )
                print(f"  /{p.name}({args}) - {p.description}")

            # 2) FETCH + FILL. get_prompt() sends the arguments and gets back
            #    fully rendered messages. The client never saw the wording.
            filled = await session.get_prompt(
                "summarize_incident",
                arguments={
                    "report": (
                        "At 02:14 UTC the checkout API began returning 503s. Root cause was a "
                        "connection-pool exhaustion after a bad deploy. 38% of checkout traffic "
                        "failed for 22 minutes. Rolled back at 02:36 UTC; error rate normal since."
                    ),
                    "audience": "executives",
                },
            )
            print("\n--- Rendered messages for /summarize_incident ---")
            chat = _to_chat_messages(filled)
            for m in chat:
                print(f"[{m['role']}] {m['content'][:200]}")

            # The structured, multi-message template.
            triage = await session.get_prompt(
                "triage_alert",
                arguments={"alert_text": "DiskUsage > 95% on db-primary-2", "severity": "sev1"},
            )
            print("\n--- Rendered messages for /triage_alert ---")
            for m in _to_chat_messages(triage):
                print(f"[{m['role']}] {m['content']}")

            # 3) USE IT. A server-rendered prompt is just messages, so it
            #    drops straight into a normal LLM call. One Groq call only —
            #    the free tier is ~8000 tokens/minute, so we pace ourselves.
            if call_llm:
                print("\n--- LLM answer to the server-provided prompt ---")
                print(get_llm().call(chat))


def demo_prompts(call_llm: bool = True) -> None:
    """Sync wrapper so main.py can call this like every other section."""
    asyncio.run(_run_client(call_llm=call_llm))


if __name__ == "__main__":
    if "--server" in sys.argv:
        # Child process: become the MCP server and block, serving over stdio.
        build_server().run(transport="stdio")
    else:
        demo_prompts()
