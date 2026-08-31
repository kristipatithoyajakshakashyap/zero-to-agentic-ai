"""
01_installation_and_first_crew - Part 3: Your First Crew
========================================================

This module builds the minimal crew: 1 agent + 1 task + sequential process.
"""

import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import requests
from crewai import LLM, Agent, Task, Crew, Process

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


def get_llm(model: str | None = None, temperature: float = 0.0, **kw) -> LLM:
    """Groq-first LLM resolver. Falls back to local Ollama only - no OpenAI.

    Beginner note: a CrewAI `Agent` needs an `llm` object to actually think.
    Rather than hardcoding one provider, this helper *checks* which provider
    is reachable right now and returns the right `LLM` object automatically:
      1. Try Groq first (fast, free-tier cloud API) - needs GROQ_API_KEY.
      2. If Groq is down/unset, try a local Ollama server (no API key needed,
         but you must have Ollama installed and running on your machine).
      3. If neither works, raise a clear error instead of failing silently
         deep inside a crew run where it's harder to debug.
    """
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            # Quick "is Groq reachable with this key" check before committing to it.
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass  # Network hiccup or Groq outage - fall through to Ollama.

    try:
        # Ollama's default local REST API - if this responds, Ollama is running.
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kw)
    except requests.RequestException:
        pass

    # Neither provider worked - stop here with a message that tells the
    # learner exactly what to fix, instead of a confusing crash later.
    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


# Resolved once at import time so every Agent in this file shares one LLM.
llm = get_llm()


def build_and_run_minimal_crew():
    """Build and run the minimal crew: 1 agent + 1 task + sequential process."""

    # Every CrewAI Agent needs three things to come alive:
    #   role      - who the agent "is" (shapes tone and expertise)
    #   goal      - what the agent is trying to achieve
    #   backstory - extra context the LLM uses to stay in character
    agent = Agent(
        role="Greeter",
        goal="Say hello to the user in a friendly way.",
        backstory=(
            "You are a warm and welcoming assistant who "
            "loves greeting people with a smile."
        ),
        llm=llm,
        allow_delegation=False,  # this agent works alone, can't hand off work
        verbose=True,  # print the agent's step-by-step thinking to the console
    )
    print("Agent created:", agent.role)

    # A Task is the actual unit of work. `expected_output` tells the LLM
    # what "done" looks like, which keeps its answer on-topic and short.
    task = Task(
        description="Greet the user by saying hello and introducing yourself.",
        expected_output="A short greeting string, 1-3 sentences.",
        agent=agent,
    )
    print("Task created for agent:", task.agent.role)

    # A Crew wires agents + tasks together and controls *how* they run.
    # Process.sequential = tasks run one after another, in list order.
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
    print("Crew created with", len(crew.agents), "agent(s) and", len(crew.tasks), "task(s).")

    print("\n--- Running Crew ---")
    result = crew.kickoff()

    print("\n=== Crew Output (raw) ===")
    print(result.raw)
    print("\n=== Token Usage ===")
    print("Prompt tokens    :", result.token_usage.prompt_tokens)
    print("Completion tokens:", result.token_usage.completion_tokens)

    print("\n=== Output Parsing ===")
    print("Type of result :", type(result).__name__)
    print("Raw output     :", repr(result.raw))
    print("Available attributes:", [attr for attr in dir(result) if not attr.startswith("_")])

    return result


def minimal_crew_template():
    """Complete minimal crew pattern in one block - reusable template."""
    print("\n" + "=" * 60)
    print("Minimal Crew Template (Complete Pattern)")
    print("=" * 60)

    template_llm = get_llm()

    solo_agent = Agent(
        role="Math Tutor",
        goal="Explain one math concept clearly in under 50 words.",
        backstory="You are a patient tutor who makes math accessible.",
        llm=template_llm,
        allow_delegation=False,
        verbose=False,
    )

    solo_task = Task(
        description="Explain what a derivative is, in plain language.",
        expected_output="A 2-4 sentence explanation a beginner can understand.",
        agent=solo_agent,
    )

    solo_crew = Crew(
        agents=[solo_agent],
        tasks=[solo_task],
        process=Process.sequential,
        verbose=False,
    )

    solo_result = solo_crew.kickoff()
    print("=== Math Tutor says ===")
    print(solo_result.raw)


if __name__ == "__main__":
    print("=" * 60)
    print("Part 3: Your First Crew")
    print("=" * 60)
    build_and_run_minimal_crew()
    minimal_crew_template()
