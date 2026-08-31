"""Task-level human_input flag: CrewAI pauses after this task to collect
human feedback before considering it complete.

BEGINNER NOTES
--------------
`hitl_flow.py` showed human approval as a whole Flow step. CrewAI also
supports a finer-grained version: setting `human_input=True` on a single
`Task` makes CrewAI itself pause after that task and ask a person for
feedback via the terminal, before marking the task complete.

CrewAI's built-in human_input path calls Python's input() under the hood,
which would block this unattended course run. This module demonstrates the
same reviewer-loop pattern explicitly instead, using an auto-approve stand-in
identical in spirit to human_input=True, so the file still runs end-to-end.

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


def reviewer_feedback(draft: str) -> str:
    """Stand-in for the human_input=True prompt CrewAI would show interactively."""
    print(f"[reviewer stand-in] Draft received ({len(draft)} chars) -> feedback: 'Looks good, ship it.'")
    return "Looks good, ship it."


def run_task_with_review(topic: str = "onboarding checklist for new engineers") -> str:
    llm = get_llm()
    writer = Agent(
        role="Writer",
        goal=f"Draft a short checklist about {topic}",
        backstory="You write concise, actionable checklists.",
        llm=llm,
        verbose=False,
    )
    task = Task(
        description=f"Write a 3-item checklist about: {topic}",
        expected_output="A 3-item checklist.",
        agent=writer,
    )
    result = Crew(agents=[writer], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    draft = str(result)

    feedback = reviewer_feedback(draft)
    return f"{draft}\n\nReviewer feedback: {feedback}"


if __name__ == "__main__":
    final = run_task_with_review()
    print("\n--- Final reviewed output ---")
    print(final)
