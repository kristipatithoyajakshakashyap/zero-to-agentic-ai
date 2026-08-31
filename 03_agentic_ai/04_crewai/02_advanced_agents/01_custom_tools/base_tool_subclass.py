"""Module 01 - Custom Tools: BaseTool subclassing for full control.

BEGINNER NOTE: The @tool decorator (see tool_decorator_basics.py) is
great for simple one-function tools. When a tool needs typed/validated
inputs, extra setup, or more structure, subclass CrewAI's `BaseTool`
instead. You declare the tool's inputs as a Pydantic model
(`args_schema`) so CrewAI validates the LLM's arguments before your
code ever runs.

Run standalone: python base_tool_subclass.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
from pathlib import Path
from typing import Type

import requests
from crewai import LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    """Groq-first, Ollama-fallback LLM builder (see tool_decorator_basics.py
    for the full explanation — repeated here so this file is self-contained)."""
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


# Pydantic model describing the tool's expected input. CrewAI shows this
# shape to the LLM and validates whatever arguments it sends before
# _run() below ever executes — this is how you get type-safe tool calls.
class SentimentToolInput(BaseModel):
    text: str = Field(..., description="Text to classify as positive, negative, or neutral")


class SentimentTool(BaseTool):
    name: str = "Sentiment Classifier"
    description: str = "Classify text sentiment using simple keyword heuristics."
    args_schema: Type[BaseModel] = SentimentToolInput

    def _run(self, text: str) -> str:
        # _run() is where the actual tool logic lives; CrewAI calls this
        # automatically once the LLM's arguments pass validation above.
        positive_words = {"good", "great", "excellent", "love", "amazing", "happy"}
        negative_words = {"bad", "terrible", "awful", "hate", "poor", "sad"}
        tokens = {w.strip(".,!?").lower() for w in text.split()}
        pos_hits = len(tokens & positive_words)
        neg_hits = len(tokens & negative_words)
        if pos_hits > neg_hits:
            return "positive"
        if neg_hits > pos_hits:
            return "negative"
        return "neutral"


def demonstrate_base_tool_subclass() -> None:
    tool = SentimentTool()
    print(f"Tool name: {tool.name}")
    print(f"Tool description: {tool.description}")

    for sample in ["This is a great and amazing course.", "This is a terrible and awful bug."]:
        print(f"'{sample}' -> {tool.run(text=sample)}")


if __name__ == "__main__":
    demonstrate_base_tool_subclass()
