"""Module 02 - Knowledge Sources: grounding an agent with a PDF document.

Same environment note as text_knowledge_source.py: this course avoids
CrewAI's built-in chromadb-backed knowledge_sources here (broken thin-client
conflict from a shared package) and instead extracts PDF text directly and
injects it into the agent's context.

Run standalone: python pdf_knowledge_source.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv
from pypdf import PdfReader

SHARED_DATA_DIR = Path(__file__).resolve().parents[3] / "data"
PDF_PATH = SHARED_DATA_DIR / "attention.pdf"


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


def extract_pdf_text(path: Path, max_chars: int = 4000) -> str:
    """Pull raw text out of a PDF with pypdf and cap its length.

    Capping matters: LLMs have a limited context window, and stuffing an
    entire large PDF into a prompt wastes tokens and can push out the
    instructions. In real RAG systems this is solved with chunking +
    retrieval; here we keep it simple with a hard character cap.
    """
    if not path.exists():
        raise FileNotFoundError(f"Expected shared course PDF at {path}")
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text[:max_chars]


def demonstrate_pdf_knowledge_source() -> None:
    """Same grounding idea as text_knowledge_source.py, but the knowledge
    comes from a PDF instead of a plain text file."""
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    pdf_text = extract_pdf_text(PDF_PATH)
    print(f"Extracted {len(pdf_text)} characters from {PDF_PATH.name}")

    analyst = Agent(
        role="Document Analyst",
        goal="Summarize the provided PDF content accurately",
        backstory=f"An analyst working only from this document excerpt:\n---\n{pdf_text}\n---",
        llm=llm,
        verbose=True,
    )
    task = Task(
        description="Write a two-sentence summary of the document excerpt provided.",
        expected_output="A two-sentence summary of the document.",
        agent=analyst,
    )
    crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_pdf_knowledge_source()
