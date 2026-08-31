"""main -- run the full capstone module end to end.

Order: spec -> agents/tasks -> sequential baseline -> Flow-based pipeline
(parallel + routing) -> HITL gate demo -> memory setup -> metrics.

    python main.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app_spec import APP_SPEC
from sequential_crew import run_sequential_pipeline
from run_pipeline import run as run_flow_and_metrics
from hitl_gate import HITLAppBuilderFlow
from memory_setup import build_memory_enabled_crew
from pathlib import Path


def main() -> None:
    print("=== Capstone: Full-Stack App Builder ===")
    print(f"Spec: {APP_SPEC['name']} -- {len(APP_SPEC['requirements'])} requirements\n")

    print("=== 1. Sequential baseline (6 agents, one after another) ===")
    run_sequential_pipeline()

    print("\n=== 2. Flow-based pipeline (parallel dev + routing) + metrics ===")
    run_flow_and_metrics()

    print("\n=== 3. Human-in-the-loop approval gate (structural demo) ===")
    HITLAppBuilderFlow().kickoff()

    print("\n=== 4. Persistent memory setup ===")
    build_memory_enabled_crew(Path(__file__).resolve().parent / ".capstone_memory")

    print("\n=== Capstone complete ===")


if __name__ == "__main__":
    main()
