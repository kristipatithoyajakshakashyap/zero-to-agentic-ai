"""CrewAI Flow persistence: @persist checkpoints flow state to SQLite so a
flow can be resumed later from the same checkpoint id.

BEGINNER NOTES
--------------
Normally a Flow's state (see 01_flows_basics/flow_state.py) only lives in
memory — once the Python process ends, it's gone. The `@persist` decorator
changes that: after every step, CrewAI automatically saves the flow's state
to a local SQLite database, keyed by a flow id. Later, you can create a new
Flow instance with that same id and it will load the saved state instead of
starting fresh. This is essential for long-running or resumable workflows
(e.g. a flow that waits days for a human approval).

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
from dotenv import load_dotenv
from pydantic import BaseModel

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"
DB_PATH = Path(__file__).resolve().parent / "flow_checkpoints.db"


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


class ChecklistState(BaseModel):
    id: str = ""
    topic: str = ""
    idea: str = ""
    plan: str = ""


@persist(persistence=None)  # None = use CrewAI's default SQLiteFlowPersistence
class ChecklistFlow(Flow[ChecklistState]):
    """Two-step flow whose state is checkpointed to SQLite after each step.

    Just adding `@persist` above the class is enough — CrewAI handles
    saving `self.state` to disk after each `@start`/`@listen` method runs,
    and loading it back when you create a new instance with a known id.
    """

    @start()
    def brainstorm(self) -> str:
        llm = get_llm()
        agent = Agent(
            role="Brainstormer",
            goal=f"Propose one concrete idea related to {self.state.topic}",
            backstory="You generate a single focused idea, no fluff.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Propose one concrete idea about: {self.state.topic}. One sentence.",
            expected_output="One sentence idea.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.idea = str(result)
        return self.state.idea

    @listen(brainstorm)
    def plan(self, idea: str) -> str:
        llm = get_llm()
        agent = Agent(
            role="Planner",
            goal="Turn an idea into a 2-step plan",
            backstory="You produce short, numbered action plans.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Turn this idea into a 2-step numbered plan:\n{idea}",
            expected_output="A 2-step numbered plan.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.plan = str(result)
        return self.state.plan


def run_and_checkpoint(topic: str = "improving code review turnaround time") -> str:
    """Run the flow once, generating a fresh flow id. Because the class is
    decorated with @persist, CrewAI writes a checkpoint row to SQLite for
    this id after every step completes."""
    flow_id = str(uuid.uuid4())  # unique id so we can find this run's checkpoint later
    flow = ChecklistFlow()
    flow.kickoff(inputs={"id": flow_id, "topic": topic})
    print(f"Checkpointed flow id: {flow_id}")
    print("Idea:", flow.state.idea)
    print("Plan:", flow.state.plan)
    return flow_id


if __name__ == "__main__":
    run_and_checkpoint()
