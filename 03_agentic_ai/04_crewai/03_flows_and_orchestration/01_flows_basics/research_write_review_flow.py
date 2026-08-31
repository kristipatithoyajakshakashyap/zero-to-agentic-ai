"""CrewAI Flow basics: @start / @listen chaining across research -> write -> review.

BEGINNER NOTES
--------------
A `Flow` is CrewAI's way of wiring multiple steps (each step can be its own
crew) into a pipeline. `@start()` marks the first method that runs. `@listen(x)`
marks a method that runs automatically once method `x` finishes, receiving
`x`'s return value as its argument. This lets you chain crews together:
research -> write -> review, where each step's output feeds the next step's
input, without you manually calling them in order.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv

from flow_state import ResearchFlowState

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


def _load_track_env() -> None:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> LLM:
    """Resolve an LLM: Groq first, local Ollama fallback. No OpenAI, ever.

    Every agent in this course needs an `LLM` object to think with. Rather
    than hardcoding one provider, this helper checks that Groq is actually
    reachable (a quick network ping to Groq's API) before using it, and
    falls back to a locally-running Ollama model if Groq isn't available.
    If neither works, it raises a clear error instead of silently guessing.
    """
    _load_track_env()  # make sure GROQ_API_KEY from .env is loaded into os.environ
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            # Ping Groq's "list models" endpoint — cheap way to confirm the key works.
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kwargs)
        except requests.RequestException:
            pass  # network hiccup or Groq down -> fall through to Ollama

    try:
        # Ollama is a free, local LLM runtime. If it's running on this machine,
        # use it as a backup so the course still works without internet/Groq.
        if requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3).status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kwargs)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


class ResearchWriteReviewFlow(Flow[ResearchFlowState]):
    """Three-step flow: research -> write -> review, each a single-agent crew.

    Each step below builds ONE agent, gives it ONE task, wraps them in a
    one-agent Crew, and runs it. This keeps each step simple and easy to
    read; in a bigger app a step could use a multi-agent crew instead.
    """

    @start()
    def research(self) -> str:
        # Step 1: this is the entry point of the flow (marked by @start()).
        # It builds a "Researcher" agent and asks it to gather facts.
        llm = get_llm()
        researcher = Agent(
            role="Researcher",
            goal=f"Gather three concise factual bullet points about {self.state.topic}",
            backstory="You are a meticulous researcher who writes short, factual notes.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Research the topic: {self.state.topic}. Produce exactly 3 bullet points.",
            expected_output="Three bullet points of factual notes.",
            agent=researcher,
        )
        result = Crew(agents=[researcher], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.research_notes = str(result)
        return self.state.research_notes

    @listen(research)
    def write(self, research_notes: str) -> str:
        # Step 2: runs automatically after `research` finishes.
        # `research_notes` is exactly what `research()` returned above —
        # this is how data flows from one flow step to the next.
        llm = get_llm()
        writer = Agent(
            role="Writer",
            goal="Turn research notes into a short paragraph",
            backstory="You are a clear, concise technical writer.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Using these research notes, write a 2-3 sentence paragraph:\n{research_notes}",
            expected_output="A 2-3 sentence paragraph.",
            agent=writer,
        )
        result = Crew(agents=[writer], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.draft = str(result)
        return self.state.draft

    @listen(write)
    def review(self, draft: str) -> str:
        # Step 3: runs after `write` finishes, receiving the draft paragraph.
        # Notice each step also writes its result onto `self.state` — that's
        # the Flow's typed state object (see flow_state.py), which is how you
        # can inspect the full history after the flow completes.
        llm = get_llm()
        reviewer = Agent(
            role="Reviewer",
            goal="Give one sentence of feedback on a draft paragraph",
            backstory="You are a supportive editor who gives brief, actionable feedback.",
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=f"Give one sentence of feedback on this draft:\n{draft}",
            expected_output="One sentence of feedback.",
            agent=reviewer,
        )
        result = Crew(agents=[reviewer], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        self.state.review_notes = str(result)
        return self.state.review_notes


def run_flow(topic: str = "the benefits of unit testing") -> ResearchFlowState:
    """Create the flow and kick it off. `inputs` seeds the initial state
    (here, `topic`) before @start() runs."""
    flow = ResearchWriteReviewFlow()
    flow.kickoff(inputs={"topic": topic})
    return flow.state


if __name__ == "__main__":
    # Running this file directly executes the whole 3-step flow end to end
    # and prints what each step produced.
    final_state = run_flow()
    print("\n--- Research notes ---")
    print(final_state.research_notes)
    print("\n--- Draft ---")
    print(final_state.draft)
    print("\n--- Review ---")
    print(final_state.review_notes)
