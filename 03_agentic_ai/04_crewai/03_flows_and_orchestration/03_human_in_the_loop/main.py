"""Run every section of 03_human_in_the_loop in sequence.

BEGINNER NOTES
--------------
Convenience runner only — see hitl_flow.py and task_level_human_input.py
for the actual teaching content. Each file also runs standalone.
"""

from __future__ import annotations

from hitl_flow import run_flow
from task_level_human_input import run_task_with_review


def main() -> None:
    print("=== hitl_flow.py ===")
    state = run_flow()
    print("Final output:", state.final_output)

    print("\n=== task_level_human_input.py ===")
    result = run_task_with_review()
    print(result)


if __name__ == "__main__":
    main()
