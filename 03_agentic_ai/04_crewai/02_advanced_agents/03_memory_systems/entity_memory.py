"""Module 03 - Memory Systems: tracking entities and relationships.

CrewAI's built-in EntityMemory is also chromadb-backed (broken here, see
short_term_memory.py note). This lesson demonstrates the same concept -- an
agent tracking named entities across a conversation -- with a plain Python
entity table the agent's task description references directly.

Run standalone: python entity_memory.py
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


class EntityTable:
    """Minimal entity tracker: name -> facts learned about it."""

    def __init__(self) -> None:
        self._entities: dict[str, list[str]] = {}

    def remember(self, entity: str, fact: str) -> None:
        self._entities.setdefault(entity, []).append(fact)

    def as_context(self) -> str:
        if not self._entities:
            return "No entities known yet."
        lines = [f"{name}: {'; '.join(facts)}" for name, facts in self._entities.items()]
        return "\n".join(lines)


def demonstrate_entity_memory() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    entities = EntityTable()
    entities.remember("Ada", "is the MLCourse mascot, a teal-colored owl")
    entities.remember("Groq", "is the LLM provider used across this course")

    agent = Agent(
        role="Entity Tracker",
        goal="Answer questions using the tracked entity table",
        backstory=f"Known entities and facts:\n{entities.as_context()}",
        llm=llm,
        verbose=True,
    )
    task = Task(
        description="What do you know about 'Ada' and 'Groq'? Answer in two short sentences.",
        expected_output="Two sentences, one per entity.",
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_entity_memory()
