"""baseline_crew -- build a minimal summarizer crew and run it once (Groq).

Establishes the "before training" baseline output that train_crew.py
later compares improved iterations against.

BEGINNER NOTE: this is the smallest possible CrewAI setup -- one Agent,
one Task, one Crew. Read this file first if CrewAI is new to you: the
`Agent` describes WHO does the work (role/goal/backstory), the `Task`
describes WHAT to do, and the `Crew` glues them together and actually
runs them when you call `.kickoff()`.

    python baseline_crew.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv


def _find_track() -> Path:
    p = Path(__file__).resolve()
    while p.name != "03_agentic_ai" and p.parent != p:
        p = p.parent
    return p


TRACK = _find_track()
load_dotenv(TRACK / ".env", override=False)


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.7, **kw) -> LLM:
    """Groq-first LLM resolver. Falls back to local Ollama. No OpenAI."""
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
        "No LLM provider reachable. Set GROQ_API_KEY in 03_agentic_ai/.env or run local Ollama."
    )


def build_crew() -> Crew:
    llm = get_llm()
    summarizer = Agent(
        role="Content Summarizer",
        goal="Produce a clear, accurate one-paragraph summary of the given topic.",
        backstory=(
            "You are an expert summarizer. You distill complex topics into a "
            "single well-structured paragraph that captures the key points."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )
    summarize_task = Task(
        description=(
            "Write a one-paragraph summary of the following topic: {topic}. "
            "The summary must be exactly 3-5 sentences long, factual, and "
            "contain no markdown formatting."
        ),
        expected_output="A plain text paragraph of 3-5 sentences.",
        agent=summarizer,
    )
    return Crew(agents=[summarizer], tasks=[summarize_task], process=Process.sequential, verbose=False)


def run_baseline(topic: str = "reinforcement learning") -> str:
    crew = build_crew()
    start = time.time()
    result = crew.kickoff(inputs={"topic": topic})
    elapsed = time.time() - start
    print(f"Baseline output ({elapsed:.1f}s):")
    print("-" * 60)
    print(str(result))
    print("-" * 60)
    return str(result)


if __name__ == "__main__":
    run_baseline()
