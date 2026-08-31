"""hitl_gate -- a human-in-the-loop (HITL) approval gate, added after the
Architect step and before development begins.

BEGINNER NOTE: in production you'd pause here and wait for a real person
(via a Slack message, a web dashboard, an email) to approve or reject the
architecture before any code gets generated -- that's expensive to redo,
so a human should sign off first. Because this course must run
unattended (no one is sitting at a terminal to type "yes"), the gate here
auto-approves and prints exactly what a real approval step would show a
human, so you can see the shape of the pattern without it blocking.

    python hitl_gate.py
"""

from __future__ import annotations

import sys

from crewai.flow.flow import Flow, listen, start

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class HITLAppBuilderFlow(Flow):
    """A trimmed-down flow that demonstrates the approval-gate pattern.

    Real work (calling agents) is skipped here -- this file's only job is
    to show *where* and *how* a human approval step plugs into a Flow.
    See flow_orchestration.py for the full pipeline with real agents.
    """

    @start()
    def start_pipeline(self):
        print("[Flow] Starting pipeline")
        return "PM output placeholder"

    @listen(start_pipeline)
    def design_architecture(self, pm_output):
        print("[Flow] Architect designing system...")
        return "Architecture design complete"

    @listen(design_architecture)
    def human_approval_gate(self, arch_output):
        """The approval gate. In production this would call out to a real
        human (Slack/webhook/dashboard) and block until they respond."""
        print("\n" + "=" * 60)
        print("HUMAN-IN-THE-LOOP APPROVAL GATE")
        print("=" * 60)
        print("Architecture design complete. A human would review it here.")
        print("This course runs unattended, so we auto-approve and log it clearly:")

        approved = True  # non-interactive stand-in for a real approval call
        print(f"[HITL] auto-approved={approved} (would be a real human decision in production)")

        return arch_output if approved else None

    @listen(human_approval_gate)
    def develop_frontend(self, arch_output):
        if arch_output is None:
            print("[Flow] Pipeline stopped -- human rejected the architecture")
            return None
        print("[Flow] Frontend development proceeds")
        return "Frontend code"

    @listen(human_approval_gate)
    def develop_backend(self, arch_output):
        if arch_output is None:
            return None
        print("[Flow] Backend development proceeds")
        return "Backend code"


if __name__ == "__main__":
    flow = HITLAppBuilderFlow()
    result = flow.kickoff()
    print(f"\nHITL flow completed. Final output: {result}")
