"""agents -- the six specialist agents of the capstone pipeline.

BEGINNER NOTE: creating an Agent object does NOT call the LLM yet -- it
just configures who the agent is (role/goal/backstory) and which LLM it
will use once a Task actually runs. That's why this file is safe and fast
to run on its own: no network calls happen until a Crew.kickoff() runs.

Provider: Groq (fast cloud), falling back to local Ollama. Never OpenAI.

    python agents.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from crewai import LLM, Agent
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _find_track() -> Path:
    p = Path(__file__).resolve()
    while p.name != "03_agentic_ai" and p.parent != p:
        p = p.parent
    return p


load_dotenv(_find_track() / ".env", override=False)


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.7, **kw) -> LLM:
    """Groq-first LLM resolver with a local-Ollama fallback. No OpenAI."""
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            if requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            ).status_code == 200:
                return LLM(model=f"groq/{model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass
    try:
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass
    raise RuntimeError("No LLM provider reachable. Set GROQ_API_KEY in 03_agentic_ai/.env or run local Ollama.")


def build_agents() -> dict[str, Agent]:
    """Construct all six agents, each sharing the same resolved LLM.

    Each agent gets a role (job title), a goal (what success looks like),
    and a backstory (personality/expertise the LLM roleplays as) -- these
    three fields are the main levers CrewAI gives you to shape behavior.
    """
    llm = get_llm()

    pm_agent = Agent(
        role="Product Manager",
        goal="Parse the application specification into structured user stories with acceptance criteria.",
        backstory="You are an experienced product manager who translates requirements into clear user stories.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    architect_agent = Agent(
        role="System Architect",
        goal="Design the system architecture, database schema, and API contracts.",
        backstory="You are a senior software architect who produces clear, implementable technical specs.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    frontend_agent = Agent(
        role="Frontend Developer",
        goal="Generate React TypeScript components implementing the UI.",
        backstory="You are a skilled React developer who writes clean, typed, production-ready code.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    backend_agent = Agent(
        role="Backend Developer",
        goal="Generate FastAPI Python endpoints implementing the API.",
        backstory="You are an expert Python developer specializing in FastAPI, Pydantic, and SQLAlchemy.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    qa_agent = Agent(
        role="QA Engineer",
        goal="Write comprehensive tests and report bugs.",
        backstory="You are a meticulous QA engineer who tests happy paths, edge cases, and error conditions.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    writer_agent = Agent(
        role="Technical Writer",
        goal="Create README and API documentation.",
        backstory="You are a technical writer who creates clear, concise documentation.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    return {
        "pm": pm_agent,
        "architect": architect_agent,
        "frontend": frontend_agent,
        "backend": backend_agent,
        "qa": qa_agent,
        "writer": writer_agent,
    }


if __name__ == "__main__":
    agents = build_agents()
    print(f"All {len(agents)} agents defined:")
    for key, agent in agents.items():
        print(f"  {key:10s} -> {agent.role}")
