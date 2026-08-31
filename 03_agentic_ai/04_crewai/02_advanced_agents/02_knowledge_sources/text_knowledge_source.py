"""Module 02 - Knowledge Sources: grounding an agent with a text file.

Note: this environment has a conflicting `chromadb-client` package installed
alongside full `chromadb` (used elsewhere for RAG), which forces ChromaDB
into a broken thin-client mode. Rather than touch shared packages, this
module demonstrates knowledge grounding by loading the source file's content
directly into the agent's context -- the same practical effect CrewAI's
built-in knowledge_sources gives you, without requiring local vector storage.

Run standalone: python text_knowledge_source.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge" / "course_facts.txt"


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Resolve which LLM backend to use: Groq first, local Ollama as fallback.

    Every module in this course repeats this same small helper on purpose
    (no shared file) so each module stays copy-paste runnable on its own.
    It never falls back to OpenAI -- if neither Groq nor Ollama answers, it
    raises a clear error instead of silently switching provider.
    """
    # Walk up the folder tree until we find 03_agentic_ai/, then load its .env.
    # This lets every module find the shared GROQ_API_KEY no matter how deep
    # its own folder sits inside the course.
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            # A quick "is Groq reachable with this key" check before committing
            # to it, so a bad/expired key fails over to Ollama instead of
            # blowing up mid-crew.
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
        # No cloud key, or Groq unreachable -> try a local Ollama server.
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env "
        "or run a local Ollama server."
    )


def load_knowledge_text(path: Path) -> str:
    """Read the knowledge file's raw text so it can be handed to the agent."""
    return path.read_text(encoding="utf-8")


def demonstrate_text_knowledge_source() -> None:
    """Show the core idea of 'knowledge grounding': give an agent facts it
    didn't learn during training, and it will answer using those facts
    instead of guessing or hallucinating.

    CrewAI normally does this with a `knowledge_sources=[...]` parameter on
    the Agent/Crew that embeds the file into a vector store and retrieves
    relevant chunks at run time. Here we get the same *practical* effect the
    simple way: read the file and paste its contents straight into the
    agent's backstory, so the model always has the facts in context.
    """
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    knowledge_text = load_knowledge_text(KNOWLEDGE_FILE)
    print(f"Loaded knowledge file ({len(knowledge_text)} chars) from {KNOWLEDGE_FILE.name}")

    # The backstory is where we "ground" the agent: by embedding the fact
    # sheet directly in its backstory, every answer it gives is checked
    # against this text rather than the model's general training data.
    assistant = Agent(
        role="Course Assistant",
        goal="Answer questions using only the facts provided in the knowledge context",
        backstory=(
            "An assistant that only trusts the following course fact sheet:\n"
            f"---\n{knowledge_text}\n---"
        ),
        llm=llm,
        verbose=True,
    )
    # Ask something that can ONLY be answered correctly if the agent actually
    # used the knowledge file -- proves the grounding worked.
    task = Task(
        description="What color is the course mascot and what is its name? Answer in one short sentence.",
        expected_output="One sentence naming the mascot's color and name.",
        agent=assistant,
    )
    crew = Crew(agents=[assistant], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_text_knowledge_source()
