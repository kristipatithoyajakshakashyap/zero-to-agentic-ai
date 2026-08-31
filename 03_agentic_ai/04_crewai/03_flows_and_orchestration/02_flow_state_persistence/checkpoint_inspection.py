"""Resume a persisted CrewAI Flow from its checkpoint and inspect stored state.

BEGINNER NOTES
--------------
This file shows the "other half" of persistence: reading a checkpoint back.
`SQLiteFlowPersistence` is the same storage class CrewAI uses internally
when you add `@persist` to a Flow — here we use it directly to peek at what
got saved. Then we create a brand-new `ChecklistFlow()` instance and pass
the *same* flow id back in, which makes CrewAI load the saved state instead
of starting the flow over from scratch.

Run persisted_flow.py first to create a checkpoint, or this script will
create its own checkpoint on the fly, then resume from that exact flow id.
"""

from __future__ import annotations

from crewai.flow.persistence.sqlite import SQLiteFlowPersistence

from persisted_flow import ChecklistFlow, run_and_checkpoint


def inspect_checkpoint(flow_id: str) -> dict:
    """Read the raw saved state for a flow id directly from SQLite —
    useful for debugging or building an admin dashboard over saved runs."""
    persistence = SQLiteFlowPersistence()
    state = persistence.load_state(flow_id)
    return state or {}


def resume_flow(flow_id: str) -> ChecklistFlow:
    """Re-create a Flow instance; @persist rehydrates its state from the
    given checkpoint id instead of starting fresh. Passing the SAME id used
    in a previous run is what triggers the "resume" behavior."""
    flow = ChecklistFlow()
    flow.kickoff(inputs={"id": flow_id})
    return flow


if __name__ == "__main__":
    flow_id = run_and_checkpoint(topic="reducing on-call alert fatigue")

    print("\n--- Stored checkpoint row ---")
    stored = inspect_checkpoint(flow_id)
    print(f"Checkpoint keys: {list(stored.keys())}")

    print("\n--- Resuming flow from checkpoint ---")
    resumed = resume_flow(flow_id)
    print("Resumed idea:", resumed.state.idea)
    print("Resumed plan:", resumed.state.plan)
