"""Run multiple independent crews concurrently with kickoff_async +
asyncio.gather, instead of one after another.

BEGINNER NOTES
--------------
`crew.kickoff()` runs synchronously and blocks until done. `crew.kickoff_async()`
returns an awaitable instead, so you can start several crews at once with
`asyncio.gather()` and let their LLM calls happen in parallel — much faster
than looping over `kickoff()` calls one at a time when the crews don't
depend on each other's output.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import asyncio
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


def _build_single_agent_crew(topic: str) -> Crew:
    """One small helper crew: a single agent answering one topic in one sentence."""
    llm = get_llm()
    agent = Agent(
        role="Researcher",
        goal=f"Answer a question about {topic} in one sentence",
        backstory="You give crisp, single-sentence answers.",
        llm=llm,
        verbose=False,
    )
    task = Task(
        description=f"In one sentence, explain: {topic}",
        expected_output="One sentence.",
        agent=agent,
    )
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)


async def run_parallel_crews(topics: list[str] | None = None) -> list[str]:
    topics = topics or [
        "what a load balancer does",
        "what an index does in a database",
        "what a CDN does",
    ]
    crews = [_build_single_agent_crew(topic) for topic in topics]

    # kickoff_async() on each crew returns a coroutine immediately without
    # running it; asyncio.gather() then runs all of them concurrently and
    # waits for every one to finish.
    results = await asyncio.gather(*(crew.kickoff_async() for crew in crews))
    return [str(result) for result in results]


if __name__ == "__main__":
    outputs = asyncio.run(run_parallel_crews())
    for i, output in enumerate(outputs, start=1):
        print(f"--- Crew {i} result ---")
        print(output)
