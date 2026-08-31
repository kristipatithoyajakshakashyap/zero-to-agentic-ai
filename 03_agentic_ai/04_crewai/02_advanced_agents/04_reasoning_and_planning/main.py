"""Module 04 - Reasoning and Planning: run every section in sequence.

Run: python main.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from agent_reasoning import demonstrate_agent_reasoning
from crew_planning import demonstrate_crew_planning
from reasoning_plus_planning import demonstrate_reasoning_plus_planning


def main() -> None:
    print("\n--- 1. Agent-level reasoning ---")
    demonstrate_agent_reasoning()

    print("\n--- 2. Crew-level planning ---")
    demonstrate_crew_planning()

    print("\n--- 3. Reasoning + planning combined ---")
    demonstrate_reasoning_plus_planning()


if __name__ == "__main__":
    main()
