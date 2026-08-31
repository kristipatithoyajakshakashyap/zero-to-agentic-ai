"""Module 04 - Reasoning and Planning: combining agent reasoning with crew planning.

Run standalone: python reasoning_plus_planning.py
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


def demonstrate_reasoning_plus_planning() -> None:
    """When to use which:
    - reasoning=True (agent-level): the AGENT thinks through ITS OWN task before answering.
    - planning=True (crew-level): the CREW breaks the whole task list into a plan before execution starts.
    Use both together for crews doing multi-step, non-trivial work.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    strategist = Agent(
        role="Pricing Strategist",
        goal="Recommend a price for a new product after reasoning through market factors",
        backstory="A strategist who reasons before recommending numbers.",
        llm=llm,
        reasoning=True,
        max_reasoning_attempts=2,
        verbose=True,
    )
    task = Task(
        description=(
            "A competitor sells a similar product at $40. Our production cost is $15. "
            "Recommend a launch price and justify it in one sentence."
        ),
        expected_output="A price and a one-sentence justification.",
        agent=strategist,
    )
    crew = Crew(
        agents=[strategist],
        tasks=[task],
        process=Process.sequential,
        planning=True,
        planning_llm=llm,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Result (reasoning + planning combined) ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_reasoning_plus_planning()
