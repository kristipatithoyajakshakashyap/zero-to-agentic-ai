"""Run every section of 05_delegation_and_parallel_crews in sequence.

BEGINNER NOTES
--------------
Convenience runner only — see delegation_crew.py, parallel_crews.py, and
fan_out_fan_in_flow.py for the actual teaching content. Each file also
runs standalone.
"""

from __future__ import annotations

import asyncio

from delegation_crew import run_delegation_crew
from fan_out_fan_in_flow import run_flow
from parallel_crews import run_parallel_crews


def main() -> None:
    print("=== delegation_crew.py ===")
    print(run_delegation_crew())

    print("\n=== parallel_crews.py ===")
    for i, output in enumerate(asyncio.run(run_parallel_crews()), start=1):
        print(f"Crew {i}:", output)

    print("\n=== fan_out_fan_in_flow.py ===")
    state = run_flow()
    print("Summary:", state.summary)


if __name__ == "__main__":
    main()
