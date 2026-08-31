"""Agent-to-agent delegation: a supervisor agent hands off sub-work to a
specialist agent instead of doing everything itself.

BEGINNER NOTES
--------------
Setting `allow_delegation=True` on an agent gives it access to two special
built-in tools: "Delegate work to co-worker" and "Ask question to
co-worker". The agent's LLM decides on its own, based on the task, whether
to do the work itself or hand it off to a teammate — you don't write any
explicit routing logic. This models a real team where a generalist manager
loops in a specialist rather than trying to know everything themselves.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

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


def run_delegation_crew(topic: str = "the tradeoffs between REST and GraphQL") -> str:
    llm = get_llm()

    # allow_delegation=True is the whole trick: this agent CAN hand off work
    # to any other agent in the same crew if it decides that's the better move.
    supervisor = Agent(
        role="Supervisor",
        goal=f"Produce a well-rounded answer about {topic}, delegating technical depth to a specialist",
        backstory=(
            "You are a generalist team lead. You know a little about everything "
            "but you delegate deep technical questions to your specialist teammate."
        ),
        llm=llm,
        allow_delegation=True,
        verbose=False,
    )
    specialist = Agent(
        role="Technical Specialist",
        goal="Provide precise, technically accurate answers when asked",
        backstory="You are a backend engineer with deep API design expertise.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    task = Task(
        description=(
            f"Write a 3-sentence answer about: {topic}. "
            "If you need technical precision, delegate the technical part to your specialist teammate."
        ),
        expected_output="A 3-sentence answer.",
        agent=supervisor,
    )

    # Both agents must be listed on the crew so the supervisor has someone to delegate to.
    result = Crew(
        agents=[supervisor, specialist],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    ).kickoff()
    return str(result)


if __name__ == "__main__":
    print(run_delegation_crew())
