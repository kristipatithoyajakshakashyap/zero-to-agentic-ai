"""Run every section of 01_flows_basics in sequence.

BEGINNER NOTES
--------------
This file just imports and calls the other files in this folder, one after
another, so you can see the whole module's output in one run. Each file is
still runnable on its own (`python flow_state.py`, `python
research_write_review_flow.py`) — this main.py is only a convenience runner.
"""

from __future__ import annotations

from flow_state import ResearchFlowState
from research_write_review_flow import run_flow


def main() -> None:
    print("=== flow_state.py ===")
    print(ResearchFlowState(topic="demo").model_dump_json(indent=2))

    print("\n=== research_write_review_flow.py ===")
    state = run_flow()
    print("Final draft:", state.draft)


if __name__ == "__main__":
    main()
