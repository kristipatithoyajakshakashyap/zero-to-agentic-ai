"""Module 02 - Knowledge Sources: querying knowledge without a crew.

Sometimes you just want to ground a single LLM call in a document, no
Agent/Task/Crew ceremony needed. This shows the minimal pattern.

Run standalone: python direct_retrieval.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM
from dotenv import load_dotenv

KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge" / "course_facts.txt"


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


def answer_from_document(llm: LLM, question: str, document_text: str) -> str:
    """Call the LLM directly with the document text stuffed into the
    prompt -- no Agent, Task, or Crew object involved. This is the
    lowest-level way to "ground" an answer, useful when the full
    CrewAI orchestration is more than you need for a one-off question.
    """
    prompt = (
        f"Answer the question using ONLY the document below. "
        f"If the answer isn't in the document, say so.\n\n"
        f"Document:\n{document_text}\n\nQuestion: {question}"
    )
    return llm.call(prompt)


def demonstrate_direct_retrieval() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    document_text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    answer = answer_from_document(llm, "What LLM model does this course recommend?", document_text)
    print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    demonstrate_direct_retrieval()
