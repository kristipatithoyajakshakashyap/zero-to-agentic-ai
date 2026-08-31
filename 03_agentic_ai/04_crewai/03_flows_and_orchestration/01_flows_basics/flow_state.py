"""Typed state shared by the research -> write -> review Flow.

BEGINNER NOTES
--------------
CrewAI Flows carry a "state" object between steps — think of it as a shared
notebook every step can read from and write to. Using a Pydantic `BaseModel`
(instead of a plain dict) means every field has a declared type and a
default value, so typos and missing fields are caught early instead of
causing confusing bugs deep inside a flow run.

Run standalone to sanity-check the state model in isolation.
"""

from __future__ import annotations

from pydantic import BaseModel


class ResearchFlowState(BaseModel):
    """One field per piece of data the flow accumulates as it runs."""

    topic: str = ""            # what the user asked the flow to work on
    research_notes: str = ""   # filled in after the "research" step
    draft: str = ""            # filled in after the "write" step
    review_notes: str = ""     # filled in after the "review" step


if __name__ == "__main__":
    state = ResearchFlowState(topic="the benefits of unit testing")
    print("Initial flow state:")
    print(state.model_dump_json(indent=2))
