"""memory_setup -- how to give the capstone crew persistent memory across
runs, so it remembers past architecture decisions instead of starting
from scratch every time.

BEGINNER NOTE: CrewAI has three memory types:
  - Short-term memory: exists only during one crew.kickoff() call.
  - Long-term memory: saved to disk (SQLite), survives across runs.
  - Entity memory: remembers named "things" (people, systems, tech
    choices) the crew has talked about, so later tasks can refer back to
    them without re-explaining.

This file actually constructs a memory-enabled Crew (proving the classes
import and wire together correctly) rather than just printing a code
snippet -- but it does not run kickoff(), since that would repeat the
token-cost of sequential_crew.py for no new teaching value.

    python memory_setup.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from crewai import Crew, Process
from crewai.memory import EntityMemory, LongTermMemory, ShortTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage

from agents import build_agents
from tasks import build_tasks

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_memory_enabled_crew(memory_dir: Path) -> Crew:
    """Wire up a Crew with all three memory types backed by local files
    under `memory_dir`, so state survives between separate script runs."""
    memory_dir.mkdir(parents=True, exist_ok=True)

    agents = build_agents()
    tasks = build_tasks(agents)

    long_term_memory = LongTermMemory(storage=LTMSQLiteStorage(db_path=str(memory_dir / "long_term.db")))
    short_term_memory = ShortTermMemory(
        storage=RAGStorage(type="short_term", path=str(memory_dir / "short_term"))
    )
    entity_memory = EntityMemory(storage=RAGStorage(type="entities", path=str(memory_dir / "entities")))

    return Crew(
        agents=[agents["pm"], agents["architect"]],
        tasks=[tasks["pm"], tasks["architect"]],
        process=Process.sequential,
        memory=True,
        long_term_memory=long_term_memory,
        short_term_memory=short_term_memory,
        entity_memory=entity_memory,
        verbose=False,
    )


if __name__ == "__main__":
    memory_dir = Path(__file__).resolve().parent / ".capstone_memory"
    crew = build_memory_enabled_crew(memory_dir)

    print("=== CrewAI Memory System ===")
    print("Memory types: short-term (per-run), long-term (SQLite, persists), entity (remembered concepts)\n")
    print(f"Memory-enabled crew built with {len(crew.agents)} agents and {len(crew.tasks)} tasks.")
    print(f"memory={crew.memory}")
    print(f"Long-term storage file: {memory_dir / 'long_term.db'}")
    print(f"Short-term storage dir: {memory_dir / 'short_term'}")
    print(f"Entity storage dir:     {memory_dir / 'entities'}")
    print("\n(This file wires up memory but does not run kickoff() -- see")
    print("sequential_crew.py or run_pipeline.py for a live, memory-enabled run.)")
