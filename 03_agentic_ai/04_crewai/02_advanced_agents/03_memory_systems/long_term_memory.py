"""Module 03 - Memory Systems: persistence across separate crew runs.

Uses CrewAI's LTMSQLiteStorage directly (SQLite-backed, no chromadb, works
fine in this environment) to show insights persisting between two separate
kickoff() calls.

Run standalone: python long_term_memory.py
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


def demonstrate_long_term_memory() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    # LTMSQLiteStorage writes to a real .db file on disk -- unlike
    # short-term memory (which only lives for one crew.kickoff() call),
    # this survives between separate Python process runs. That's the
    # whole point of "long-term" memory.
    storage = LTMSQLiteStorage(db_path=DB_PATH)
    task_key = "favorite_language_survey"

    # First run: this will find nothing. Run the file again afterwards and
    # you'll see it print the fact saved from the previous run below.
    prior = storage.load(task_key, latest_n=1)
    if prior:
        print(f"Found {len(prior)} prior memory entr(y/ies) from an earlier run:")
        for entry in prior:
            print(f"  - {entry['metadata']}")
    else:
        print("No prior memory found -- this is the first run.")

    agent = Agent(
        role="Survey Analyst",
        goal="State a fun fact about Python in one sentence",
        backstory="An analyst who shares one new Python fact each run.",
        llm=llm,
        verbose=True,
    )
    task = Task(
        description="Share one interesting fact about the Python programming language, in one sentence.",
        expected_output="One sentence with a Python fact.",
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== This run's result ===")
    print(result.raw)

    storage.save(
        task_description=task_key,
        metadata={"fact": result.raw},
        datetime=datetime.now(timezone.utc).isoformat(),
        score=1,
    )
    print(f"\nSaved this run's fact to {DB_PATH} for the next run to recall.")


if __name__ == "__main__":
    demonstrate_long_term_memory()
