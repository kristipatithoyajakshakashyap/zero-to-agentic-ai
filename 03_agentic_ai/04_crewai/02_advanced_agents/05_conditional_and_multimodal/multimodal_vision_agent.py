"""Module 05 - Conditional and Multimodal: image-understanding with a vision LLM.

EXCEPTION TO THE GROQ-ONLY RULE: this is the one file in the whole course
that uses OpenAI. Groq does not currently expose any vision-capable chat
model on this account (verified against /v1/models), and Groq has no
image-generation API at all -- so there is no Groq path for multimodal
image understanding. OPENAI_API_KEY is used here specifically for that,
via crewai's multimodal Agent support (multimodal=True + an image_url
content block). DALL-E-style image *generation* is dropped entirely (out
of scope for this lesson, and Groq can't do it either). Every other file
in this course uses Groq only.

Run standalone: python multimodal_vision_agent.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

SAMPLE_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/"
    "Gfp-wisconsin-madison-the-nature-boardwalk.jpg/640px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
)


def get_vision_llm(model: str = "gpt-4o-mini", temperature: float = 0.0) -> LLM:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Vision support in this module requires OPENAI_API_KEY in "
            "03_agentic_ai/.env (Groq has no vision-capable model on this "
            "account and no image-generation API)."
        )
    return LLM(model=f"openai/{model}", api_key=api_key, temperature=temperature)


def build_multimodal_agent(llm: LLM) -> Agent:
    """multimodal=True tells CrewAI this agent can receive image content
    (a URL or base64 image) inside a task description, not just text."""
    return Agent(
        role="Visual Analyst",
        goal="Describe images accurately and concisely",
        backstory="An analyst who examines images and reports what they see.",
        llm=llm,
        multimodal=True,
        verbose=True,
    )


def demonstrate_multimodal_vision() -> None:
    llm = get_vision_llm()
    print(f"Resolved vision LLM: {llm.model} (OpenAI -- the one exception in this course)")

    analyst = build_multimodal_agent(llm)
    task = Task(
        description=f"Look at this image and describe it in one sentence: {SAMPLE_IMAGE_URL}",
        expected_output="One sentence describing the image.",
        agent=analyst,
    )
    crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print("\n=== Result ===")
    print(result.raw)


if __name__ == "__main__":
    demonstrate_multimodal_vision()
