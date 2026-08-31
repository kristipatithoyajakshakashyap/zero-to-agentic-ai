"""sequential_crew -- the simplest way to run all six agents: one after
another, in a fixed order. This is the baseline we compare Flow-based
parallel orchestration against in flow_orchestration.py.

BEGINNER NOTE: `Process.sequential` just means "run task 1, wait for it to
finish, then run task 2, etc." It's the easiest orchestration to reason
about, but it can't run independent tasks (like Frontend and Backend) in
parallel -- that's what Flows are for.

    python sequential_crew.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from crewai import Crew, Process

from agents import build_agents
from app_spec import spec_as_text
from tasks import build_tasks

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_sequential_pipeline() -> str:
    agents = build_agents()
    tasks = build_tasks(agents)

    crew = Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        process=Process.sequential,
        verbose=False,
    )

    print(f"Sequential crew assembled: {len(crew.agents)} agents, {len(crew.tasks)} tasks")
    print("Running sequential pipeline (6 short LLM calls, one per agent)...")

    start_time = time.time()
    result = None
    for attempt in range(4):
        try:
            result = crew.kickoff(inputs={"spec": spec_as_text()})
            break
        except Exception as exc:  # noqa: BLE001 - Groq rate limits surface as generic litellm errors
            if "rate_limit" in str(exc).lower() and attempt < 3:
                delay = 10.0 * (attempt + 1)
                print(f"  Rate limited, retrying in {delay:.0f}s...")
                time.sleep(delay)
                continue
            raise
    elapsed = time.time() - start_time

    print(f"Sequential pipeline completed in {elapsed:.1f}s")
    print(f"Output length: {len(str(result))} chars")

    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    result_file = data_dir / "capstone_sequential_result.txt"
    result_file.write_text(str(result), encoding="utf-8")
    print(f"Result saved to: {result_file}")

    return str(result)


if __name__ == "__main__":
    run_sequential_pipeline()
