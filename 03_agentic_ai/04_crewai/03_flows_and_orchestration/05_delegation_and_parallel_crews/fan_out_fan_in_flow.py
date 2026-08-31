"""Fan-out / fan-in orchestration: one Flow step kicks off several crews in
parallel (fan-out), then a final step combines all their results (fan-in).

BEGINNER NOTES
--------------
This combines two ideas from this module: parallel_crews.py's concurrent
kickoff_async() calls, wired into a Flow (see 01_flows_basics) so the
"gather results" step is triggered automatically once all the parallel work
finishes. This pattern is common for "research N sub-topics, then write one
combined summary" style workflows.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import asyncio
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

SUB_TOPICS = ["caching", "rate limiting", "authentication"]


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


def _build_note_crew(sub_topic: str) -> Crew:
    llm = get_llm()
    agent = Agent(
        role="Researcher",
        goal=f"Write one sentence about {sub_topic} in API design",
        backstory="You give crisp, single-sentence notes.",
        llm=llm,
        verbose=False,
    )
    task = Task(
        description=f"In one sentence, explain the role of {sub_topic} in API design.",
        expected_output="One sentence.",
        agent=agent,
    )
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)


class FanOutFanInState(BaseModel):
    sub_notes: list[str] = []
    summary: str = ""


class FanOutFanInFlow(Flow[FanOutFanInState]):
    """Fan out to N parallel crews, then fan in to a single summary step."""

    @start()
    async def fan_out_research(self) -> list[str]:
        # CrewAI Flow already runs inside an event loop, so this step is
        # itself an async method — we can `await` directly instead of
        # calling asyncio.run() (which would fail with a loop already running).
        crews = [_build_note_crew(topic) for topic in SUB_TOPICS]
        results = await asyncio.gather(*(crew.kickoff_async() for crew in crews))
        notes = [str(r) for r in results]
        self.state.sub_notes = notes
        return notes

    @listen(fan_out_research)
    def fan_in_summary(self, sub_notes: list[str]) -> str:
        # This step only runs once ALL the parallel crews above have finished —
        # that's the "fan-in": combining N parallel results into one output.
        llm = get_llm()
        agent = Agent(
            role="Summarizer",
            goal="Combine several notes into one short paragraph",
            backstory="You merge disparate notes into one coherent paragraph.",
            llm=llm,
            verbose=False,
        )
        joined = "\n".join(f"- {note}" for note in sub_notes)
        task = Task(
            description=f"Combine these notes into one 2-sentence paragraph:\n{joined}",
            expected_output="A 2-sentence paragraph.",
            agent=agent,
        )
        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.summary = str(result)
        return self.state.summary


def run_flow() -> FanOutFanInState:
    flow = FanOutFanInFlow()
    flow.kickoff()
    return flow.state


if __name__ == "__main__":
    state = run_flow()
    print("--- Individual notes (fan-out) ---")
    for note in state.sub_notes:
        print("-", note)
    print("\n--- Combined summary (fan-in) ---")
    print(state.summary)
