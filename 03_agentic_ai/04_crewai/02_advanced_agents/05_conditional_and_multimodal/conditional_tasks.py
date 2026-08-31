"""Module 05 - Conditional and Multimodal: branching task execution.

ConditionalTask only runs if a condition function returns True based on the
previous task's output -- lets a crew route down different paths.

Run standalone: python conditional_tasks.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Resolve Groq first, local Ollama as fallback. Never OpenAI."""
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


# A "condition function" takes the previous task's output and returns
# True/False. CrewAI only runs a ConditionalTask if its condition is True --
# this is how a crew "branches" like an if/else statement.
def is_positive_sentiment(output: TaskOutput) -> bool:
    return "positive" in output.raw.lower()


def is_negative_sentiment(output: TaskOutput) -> bool:
    return "negative" in output.raw.lower()


def build_conditional_crew(llm: LLM, review_text: str) -> Crew:
    """One task classifies sentiment, then two ConditionalTasks compete to
    run next -- only the one whose condition matches the classification
    actually executes. Only one of thank_you_task/apology_task will run
    per review.
    """
    classifier = Agent(
        role="Sentiment Classifier",
        goal="Classify a review as exactly one word: positive or negative",
        backstory="A classifier that always answers with exactly one word.",
        llm=llm,
        verbose=True,
    )
    responder = Agent(
        role="Customer Response Writer",
        goal="Write a short reply matching the sentiment of the review",
        backstory="A support agent who writes brief, warm replies.",
        llm=llm,
        verbose=True,
    )

    classify_task = Task(
        description=f"Classify the sentiment of this review as exactly one word (positive or negative): '{review_text}'",
        expected_output="Exactly one word: positive or negative.",
        agent=classifier,
    )
    thank_you_task = ConditionalTask(
        description="Write a short thank-you reply to a happy customer.",
        expected_output="A one-sentence thank-you reply.",
        agent=responder,
        condition=is_positive_sentiment,
    )
    apology_task = ConditionalTask(
        description="Write a short apologetic reply offering to make things right for an unhappy customer.",
        expected_output="A one-sentence apologetic reply.",
        agent=responder,
        condition=is_negative_sentiment,
    )

    return Crew(
        agents=[classifier, responder],
        tasks=[classify_task, thank_you_task, apology_task],
        process=Process.sequential,
        verbose=True,
    )


def demonstrate_conditional_tasks() -> None:
    llm = get_llm()
    print(f"Resolved LLM: {llm.model}")

    for review in [
        "This product exceeded my expectations, I love it!",
        "This product broke after one day, very disappointed.",
    ]:
        print(f"\n--- Review: {review!r} ---")
        crew = build_conditional_crew(llm, review)
        result = crew.kickoff()
        print(f"Final output: {result.raw}")


if __name__ == "__main__":
    demonstrate_conditional_tasks()
