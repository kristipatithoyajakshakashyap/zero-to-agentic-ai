"""CrewAI Flow with a human-approval gate between two steps.

BEGINNER NOTES
--------------
"Human in the loop" means an AI workflow pauses at some point and waits for
a real person to approve, reject, or edit before continuing — important
whenever mistakes are costly (sending an email, spending money, publishing
content). Here that's modeled as a flow step (`gate_on_approval`) that sits
between drafting and finalizing.

This runs unattended (no real stdin prompt), so the approval gate is a
clearly-labeled auto-approve callback standing in for a human reviewer.
Swap `auto_approve` for a real input()-based function to use this
interactively.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from pydantic import BaseModel

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


def _load_track_env() -> None:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> LLM:
    """Resolve an LLM: Groq first, local Ollama fallback. No OpenAI, ever."""
    _load_track_env()
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kwargs)
        except requests.RequestException:
            pass

    try:
        if requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3).status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kwargs)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


def auto_approve(proposal: str) -> bool:
    """Stand-in for a human reviewer: approves any non-empty proposal.

    Replace this with a real input("Approve? [y/n] ") in an interactive
    session; this course runs unattended so it must not block on stdin.
    """
    print(f"[auto-approve] Reviewing proposal ({len(proposal)} chars) -> APPROVED")
    return bool(proposal.strip())


class ApprovalState(BaseModel):
    topic: str = ""
    proposal: str = ""
    approved: bool = False
    final_output: str = ""


class HumanApprovalFlow(Flow[ApprovalState]):
    """Draft a proposal, then gate the next step behind human approval."""

    @start()
    def draft_proposal(self) -> str:
        llm = get_llm()
        agent = Agent(
            role="Proposer",
            goal=f"Draft a one-sentence proposal about {self.state.topic}",
            backstory="You draft short, actionable proposals.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Draft a one-sentence proposal about: {self.state.topic}",
            expected_output="One sentence proposal.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.proposal = str(result)
        return self.state.proposal

    @listen(draft_proposal)
    def gate_on_approval(self, proposal: str) -> bool:
        # This is the "gate": the flow pauses here (conceptually) for a
        # decision before moving on. In a real app you might send a Slack
        # message and wait for a click; here `auto_approve` stands in.
        self.state.approved = auto_approve(proposal)
        return self.state.approved

    @listen(gate_on_approval)
    def finalize(self, approved: bool) -> str:
        # Only proceed to spend another LLM call if the gate approved it.
        if not approved:
            self.state.final_output = "Proposal rejected; no further action."
            return self.state.final_output

        llm = get_llm()
        agent = Agent(
            role="Finalizer",
            goal="Turn an approved proposal into a one-line action item",
            backstory="You convert approved proposals into concrete next steps.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Turn this approved proposal into a one-line action item:\n{self.state.proposal}",
            expected_output="One-line action item.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.final_output = str(result)
        return self.state.final_output


def run_flow(topic: str = "reducing meeting overload") -> ApprovalState:
    flow = HumanApprovalFlow()
    flow.kickoff(inputs={"topic": topic})
    return flow.state


if __name__ == "__main__":
    state = run_flow()
    print("\nProposal:", state.proposal)
    print("Approved:", state.approved)
    print("Final output:", state.final_output)
