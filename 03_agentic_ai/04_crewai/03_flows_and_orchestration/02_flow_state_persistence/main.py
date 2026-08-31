"""Run every section of 02_flow_state_persistence in sequence.

BEGINNER NOTES
--------------
Convenience runner only — see persisted_flow.py and checkpoint_inspection.py
for the actual teaching content. Each file also runs standalone.
"""

from __future__ import annotations

from checkpoint_inspection import inspect_checkpoint, resume_flow
from persisted_flow import run_and_checkpoint


def main() -> None:
    print("=== persisted_flow.py ===")
    flow_id = run_and_checkpoint()

    print("\n=== checkpoint_inspection.py ===")
    print("Stored keys:", list(inspect_checkpoint(flow_id).keys()))
    resumed = resume_flow(flow_id)
    print("Resumed idea:", resumed.state.idea)


if __name__ == "__main__":
    main()
