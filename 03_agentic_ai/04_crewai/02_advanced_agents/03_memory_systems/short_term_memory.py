"""Module 03 - Memory Systems: within-run conversation context.

CrewAI's built-in ShortTermMemory uses a chromadb-backed RAG store, which is
broken in this environment by a conflicting `chromadb-client` package (same
note as the knowledge_sources module). This lesson demonstrates the same
concept -- carrying context forward within one crew run -- using CrewAI's
`context=[...]` task chaining, which needs no vector store at all.

Run standalone: python short_term_memory.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Resolve Groq first, local Ollama as fallback. Never OpenAI."""
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
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
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env "
        "or run a local Ollama server."
    )


def demonstrate_short_term_memory() -> None:
    """Two tasks, one agent: the second task needs to know what the first
    task decided (which city). `context=[pick_destination]` is what wires
    that memory forward -- without it, the second task would have no idea
    which city was chosen.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    analyst = Agent(
        role="Trip Planner",
        goal="Plan a trip step by step, remembering earlier decisions",
        backstory="A planner who builds an itinerary incrementally.",
        llm=llm,
        verbose=True,
    )

    pick_destination = Task(
        description="Pick one European city for a 3-day trip and state it in one sentence.",
        expected_output="One sentence naming the chosen city.",
        agent=analyst,
    )
    # context=[pick_destination] hands this task the OUTPUT of the previous
    # task as extra input -- this is CrewAI's built-in way of passing
    # short-term memory between tasks in the same run.
    pick_activity = Task(
        description="Using the city chosen in the previous task's context, suggest one must-do activity there.",
        expected_output="One sentence with the activity, referencing the chosen city.",
        agent=analyst,
        context=[pick_destination],
    )

    crew = Crew(
        agents=[analyst],
        tasks=[pick_destination, pick_activity],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Result (short-term context carried across tasks) ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_short_term_memory()
