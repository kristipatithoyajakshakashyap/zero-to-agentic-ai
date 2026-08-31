"""Module 03 - Memory Systems: short-term + long-term + entity memory together.

Combines the three lightweight patterns from this module into one crew run:
task-context chaining (short-term), SQLite persistence (long-term), and a
plain entity table (entity memory).

Run standalone: python combined_memory_demo.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from dotenv import load_dotenv

DB_PATH = str(Path(__file__).resolve().parent / "long_term_memory.db")


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


def demonstrate_combined_memory() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    storage = LTMSQLiteStorage(db_path=DB_PATH)
    task_key = "combined_memory_demo"
    prior = storage.load(task_key, latest_n=1)
    prior_note = prior[0]["metadata"]["note"] if prior else "none yet"
    print(f"Long-term memory from a previous run: {prior_note}")

    entity_facts = "Ada: teal-colored owl mascot. Groq: the LLM provider for this course."

    planner = Agent(
        role="Course Concierge",
        goal="Combine known entities and prior notes into helpful answers",
        backstory=f"Entity knowledge: {entity_facts}\nPrior run note: {prior_note}",
        llm=llm,
        verbose=True,
    )
    step_one = Task(
        description="Greet the learner and mention the course mascot by name.",
        expected_output="One friendly sentence mentioning the mascot.",
        agent=planner,
    )
    step_two = Task(
        description="Using the previous task's greeting as context, remind the learner which LLM provider this course uses.",
        expected_output="One sentence naming the LLM provider.",
        agent=planner,
        context=[step_one],
    )
    crew = Crew(agents=[planner], tasks=[step_one, step_two], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)

    storage.save(
        task_description=task_key,
        metadata={"note": f"Last run finished at {datetime.now(timezone.utc).isoformat()}"},
        datetime=datetime.now(timezone.utc).isoformat(),
        score=1,
    )


if __name__ == "__main__":
    demonstrate_combined_memory()
