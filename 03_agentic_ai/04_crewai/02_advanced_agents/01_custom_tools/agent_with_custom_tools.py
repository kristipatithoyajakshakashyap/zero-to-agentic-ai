"""Module 01 - Custom Tools: wiring custom tools into a real agent + crew.

BEGINNER NOTE: This ties the lesson together. A custom tool is only
useful once an Agent can call it during a real Task. Give the agent a
`tools=[...]` list; the LLM decides on its own, based on the tool's
name/description, when to call it while trying to complete the task.

Run standalone: python agent_with_custom_tools.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
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


@tool("Word Counter")
def word_counter(text: str) -> str:
    """Count words in a piece of text."""
    return f"{len(text.split())} words"


def build_crew_with_custom_tool(llm: LLM) -> Crew:
    editor = Agent(
        role="Copy Editor",
        goal="Count words in submitted copy and confirm it fits a 20-word limit",
        backstory="A meticulous editor who always checks word counts before approving copy.",
        llm=llm,
        tools=[word_counter],
        verbose=True,
    )
    check_task = Task(
        description=(
            "Use the Word Counter tool on this sentence: "
            "'CrewAI lets teams of specialized agents collaborate on complex tasks.' "
            "Report the exact word count and state whether it is under 20 words."
        ),
        expected_output="The word count and a yes/no verdict on the 20-word limit.",
        agent=editor,
    )
    return Crew(agents=[editor], tasks=[check_task], process=Process.sequential, verbose=True)


def demonstrate_agent_with_custom_tools() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")
    crew = build_crew_with_custom_tool(llm)
    result = crew.kickoff()
    print("\n=== Crew Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_agent_with_custom_tools()
