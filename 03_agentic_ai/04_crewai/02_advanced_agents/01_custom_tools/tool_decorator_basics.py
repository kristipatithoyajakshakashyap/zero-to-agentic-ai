"""Module 01 - Custom Tools: the @tool decorator.

BEGINNER NOTE: A "tool" in CrewAI is just a Python function an agent is
allowed to call while it works on a task (like giving a person a
calculator or a search bar). The simplest way to turn any function into
a tool CrewAI understands is the `@tool("name")` decorator shown below.
CrewAI reads the function's docstring as the tool's description, which
the LLM uses to decide when to call it.

Run standalone: python tool_decorator_basics.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM
from crewai.tools import tool
from dotenv import load_dotenv


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Build the LLM this lesson's agents will think with.

    BEGINNER NOTE: This helper is intentionally copy-pasted into every
    file in this course (no shared import) so each lesson file can be
    read and run completely on its own. It tries Groq's cloud API first
    (fast, needs GROQ_API_KEY in the .env file); if Groq isn't reachable
    it falls back to a local Ollama server (free, but must be installed
    and running on your machine). If neither is available we raise a
    clear error instead of guessing wrong and confusing you later.
    """
    # Walk up the folder tree until we find the shared .env file that
    # lives at the root of the 03_agentic_ai course track.
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            # A quick, cheap request just to check Groq is reachable
            # before we commit to using it for the real agent calls.
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if r.status_code == 200:
                return LLM(model=f"groq/{model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass

    try:
        # Fallback: a local Ollama server, if the learner has one running.
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env "
        "or run a local Ollama server."
    )


# The @tool decorator wraps a plain function into a CrewAI Tool object.
# The string "Word Counter" becomes the tool's display name; the
# docstring becomes the description the agent's LLM reads to decide
# when this tool is useful.
@tool("Word Counter")
def word_counter(text: str) -> str:
    """Count words, characters, and sentences in a piece of text."""
    words = len(text.split())
    chars = len(text)
    sentences = text.count(".") + text.count("!") + text.count("?")
    return f"words={words}, characters={chars}, sentences={sentences}"


@tool("Reverse Text")
def reverse_text(text: str) -> str:
    """Reverse the characters of the given text."""
    return text[::-1]


def demonstrate_tool_decorator() -> None:
    """Show that a @tool-wrapped function can be called two ways:
    directly like a normal function (via .run()), or later handed to an
    Agent so the LLM decides on its own when to call it.
    """
    print(f"Tool name: {word_counter.name}")
    print(f"Tool description: {word_counter.description}")
    # .run() calls the tool directly, the same way CrewAI calls it
    # internally once an agent decides to use it.
    result = word_counter.run(text="CrewAI makes building agent teams simple.")
    print(f"word_counter standalone result -> {result}")

    result2 = reverse_text.run(text="groq")
    print(f"reverse_text standalone result -> {result2}")


if __name__ == "__main__":
    # Running this file directly (not importing it) executes the demo.
    demonstrate_tool_decorator()
