"""Module 04 - Reasoning and Planning: crew-level task decomposition planning.

Run standalone: python crew_planning.py
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


def build_agents_and_tasks(llm: LLM) -> tuple[list[Agent], list[Task]]:
    """Two agents, two tasks -- the editor's task depends on the writer's
    output via context=[outline_task], same task-context pattern used for
    short-term memory earlier in this course."""
    writer = Agent(
        role="Blog Writer",
        goal="Write a short blog outline",
        backstory="A writer who plans posts before drafting them.",
        llm=llm,
        verbose=True,
    )
    editor = Agent(
        role="Editor",
        goal="Tighten the outline into 3 bullet points",
        backstory="An editor who trims outlines to the essentials.",
        llm=llm,
        verbose=True,
    )
    outline_task = Task(
        description="Draft a rough outline for a blog post about why Groq is fast for LLM inference.",
        expected_output="A rough outline (any length).",
        agent=writer,
    )
    tighten_task = Task(
        description="Tighten the outline from the previous task into exactly 3 bullet points.",
        expected_output="Exactly 3 bullet points.",
        agent=editor,
        context=[outline_task],
    )
    return [writer, editor], [outline_task, tighten_task]


def demonstrate_crew_planning() -> None:
    """Crew-level `planning=True` is different from agent-level `reasoning`:
    here a separate planning pass looks at ALL the tasks up front and adds
    extra guidance to each one before the crew starts working -- like a
    project manager reviewing the plan before the team begins, rather than
    one person thinking out loud mid-task.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    agents, tasks = build_agents_and_tasks(llm)
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        planning=True,
        planning_llm=llm,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Result (with crew-level planning=True) ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_crew_planning()
