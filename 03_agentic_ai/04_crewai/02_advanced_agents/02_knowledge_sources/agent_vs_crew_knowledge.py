"""Module 02 - Knowledge Sources: agent-scoped vs crew-shared knowledge.

Shows the difference between knowledge only one agent has (private context)
versus knowledge every agent in the crew shares (common context prepended
to every agent's backstory).

Run standalone: python agent_vs_crew_knowledge.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Resolve Groq first, local Ollama as fallback. Never OpenAI. See
    text_knowledge_source.py in this module for the full explanation."""
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if r.status_code == 200:
                return LLM(model=f"groq/{model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass

    try:
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env "
        "or run a local Ollama server."
    )


# "Crew-wide" knowledge is given to every agent -- like a company handbook
# everyone can read. "Agent-private" knowledge is only in one agent's
# backstory -- like a note only that one team member has seen.
CREW_WIDE_FACT = "Company policy: all refunds must be processed within 5 business days."
AGENT_PRIVATE_FACT = "Internal note (support agent only): VIP customers get 2 business days instead of 5."


def demonstrate_agent_vs_crew_knowledge() -> None:
    """Run two agents side by side: one has both shared + private facts,
    the other only has the shared fact. Watch how their answers differ --
    that's the visible effect of "scoping" knowledge to an agent vs a crew.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    # This agent knows the VIP exception (private fact) on top of policy.
    support_agent = Agent(
        role="Support Agent",
        goal="Answer refund questions using company policy and any private notes you have",
        backstory=(
            f"Shared company knowledge: {CREW_WIDE_FACT}\n"
            f"Private knowledge only you have: {AGENT_PRIVATE_FACT}"
        ),
        llm=llm,
        verbose=True,
    )
    # This agent only ever sees the shared policy -- it has no way to know
    # about the VIP exception, so it should answer "5 business days" for
    # everyone.
    general_agent = Agent(
        role="General Info Agent",
        goal="Answer refund questions using only company-wide policy",
        backstory=f"Shared company knowledge: {CREW_WIDE_FACT}",
        llm=llm,
        verbose=True,
    )

    vip_task = Task(
        description="A VIP customer asks how many business days their refund takes. Answer using whatever knowledge you have.",
        expected_output="A one-sentence answer with the number of business days.",
        agent=support_agent,
    )
    general_task = Task(
        description="A regular customer asks how many business days their refund takes. Answer using whatever knowledge you have.",
        expected_output="A one-sentence answer with the number of business days.",
        agent=general_agent,
    )

    crew = Crew(
        agents=[support_agent, general_agent],
        tasks=[vip_task, general_task],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_agent_vs_crew_knowledge()
