"""Connect a CrewAI agent to the local MCP stdio server (mcp_stdio_server.py)
and let the agent use its tools inside a real crew run.

BEGINNER NOTES
--------------
`MCPServerAdapter` is CrewAI's bridge to any MCP server: give it connection
parameters (here, "run this Python script and talk to it over stdio"), and
it discovers the server's tools and hands you back CrewAI-compatible `Tool`
objects you can pass straight into an `Agent(tools=...)`. The agent doesn't
need to know MCP exists — it just sees ordinary tools it can call.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv
from mcp import StdioServerParameters

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"
SERVER_SCRIPT = Path(__file__).resolve().parent / "mcp_stdio_server.py"


def _load_track_env() -> None:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> LLM:
    """Resolve an LLM: Groq first, local Ollama fallback. No OpenAI, ever."""
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


def run_mcp_agent(text: str = "the quick brown fox jumps over the lazy dog") -> str:
    # StdioServerParameters describes HOW to launch the server process:
    # run the current Python interpreter against mcp_stdio_server.py.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )

    # The `with` block starts the server subprocess, connects to it, and
    # guarantees it's shut down cleanly when the block exits (even on error).
    with MCPServerAdapter(server_params) as mcp_tools:
        print(f"Tools discovered from MCP server: {[t.name for t in mcp_tools]}")

        llm = get_llm()
        agent = Agent(
            role="Text Analyst",
            goal="Use the available tools to analyze the given text",
            backstory="You always use tools rather than guessing when a tool is available.",
            llm=llm,
            tools=mcp_tools,  # the MCP-discovered tools, used exactly like any other CrewAI tool
            verbose=False,
        )
        task = Task(
            description=(
                f"Use the word_count tool to count words in this text, then use the "
                f"reverse_text tool to reverse it. Text: '{text}'. "
                "Report both results plainly."
            ),
            expected_output="The word count and the reversed text.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        return str(result)


if __name__ == "__main__":
    output = run_mcp_agent()
    print("\n--- Agent output ---")
    print(output)
