"""Module 04 - Reasoning and Planning: agent-level chain-of-thought reasoning.

Run standalone: python agent_reasoning.py
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


def demonstrate_agent_reasoning() -> None:
    """`reasoning=True` makes the agent plan out loud before committing to an
    answer -- like a student showing their work instead of blurting out a
    guess. `max_reasoning_attempts` caps how many times it's allowed to
    re-think before it must give a final answer, so it can't loop forever.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    reasoning_agent = Agent(
        role="Math Tutor",
        goal="Solve word problems by reasoning step by step before answering",
        backstory="A tutor who always thinks through a problem before giving the final number.",
        llm=llm,
        reasoning=True,
        max_reasoning_attempts=2,
        verbose=True,
    )
    task = Task(
        description=(
            "A train travels 60 km in the first hour and 90 km in the second hour. "
            "What is its average speed over the two hours in km/h?"
        ),
        expected_output="The average speed as a single number with units.",
        agent=reasoning_agent,
    )
    crew = Crew(agents=[reasoning_agent], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result (with reasoning=True) ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_agent_reasoning()
