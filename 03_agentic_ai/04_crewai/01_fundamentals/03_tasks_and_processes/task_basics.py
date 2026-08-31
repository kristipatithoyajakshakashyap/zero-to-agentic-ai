"""
03_tasks_and_processes - Part 1: Task Basics
=======================================================

Task parameters: description, expected_output, agent, context, callback,
output_file, output_pydantic, output_json.
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TRACK = Path.cwd()
while TRACK.name != "03_agentic_ai" and TRACK != TRACK.parent:
    TRACK = TRACK.parent
load_dotenv(TRACK / ".env")

print("Setup complete. Track root:", TRACK)


from crewai import LLM, Agent, Task, Crew, Process

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


def get_llm(model: str | None = None, temperature: float = 0.0, **kw) -> LLM:
    """Groq-first LLM resolver. Falls back to local Ollama only - no OpenAI."""
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass

    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kw)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


llm = get_llm()

resp = llm.call("Reply OK")
print("[OK] LLM live:", resp[:30])


def kickoff_with_retry(crew_or_factory, max_retries: int = 4, base_delay: float = 65.0, **kickoff_kw):
    """Run crew.kickoff(), retrying on Groq's free-tier rate limit (429).

    Groq's free tier caps tokens-per-minute; chaining several crews back to
    back in this module can burst past that cap. Retry with backoff instead
    of letting the whole demo crash.

    Accepts either a ready-built Crew, or a zero-arg factory that builds a
    fresh Crew each attempt - required for crews whose kickoff() mutates
    internal state (e.g. hierarchical process auto-creates a manager agent
    on first run), where retrying the same instance would fail differently
    the second time.
    """
    import time
    from crewai import Crew

    build = crew_or_factory if callable(crew_or_factory) and not isinstance(crew_or_factory, Crew) else (lambda: crew_or_factory)

    for attempt in range(1, max_retries + 1):
        crew = build()
        try:
            return crew.kickoff(**kickoff_kw)
        except Exception as exc:  # noqa: BLE001 - litellm raises various provider errors
            if "rate_limit" in str(exc).lower() or "429" in str(exc):
                if attempt == max_retries:
                    raise
                print(f"[RATE LIMIT] Waiting {base_delay:.0f}s before retry {attempt}/{max_retries}...")
                time.sleep(base_delay)
                continue
            raise


def demonstrate_task_parameters():
    """Show all Task() parameters."""
    print("=" * 60)
    print("Task Parameters")
    print("=" * 60)

    def my_callback(output):
        """Called when the task completes. Receives the CrewOutput object."""
        print("[callback] Task finished. Output length:", len(output.raw))

    simple_task = Task(
        description="List three benefits of using AI agents in software engineering.",
        expected_output="A numbered list of exactly 3 items.",
        agent=Agent(
            role="Tech Writer",
            goal="Write clear technical content.",
            backstory="You write concise technical documentation.",
            llm=llm,
            allow_delegation=False,
            verbose=False,
        ),
        callback=my_callback,
        output_file=None,
    )

    _ = simple_task  # constructed for illustration; not kicked off here
    print("Task created for:", simple_task.agent.role)
    print("Has callback:", simple_task.callback is not None)

    print("\nTask Parameter Reference:")
    print("  description      : Natural-language instruction for the agent")
    print("  expected_output  : Format hint for the agent's response")
    print("  agent            : Which agent owns this task")
    print("  context          : Prior tasks whose outputs feed into this one")
    print("  callback         : Function called with the task output on finish")
    print("  output_file      : Path to write the result to disk")
    print("  output_pydantic  : Pydantic model to parse output into")
    print("  output_json      : Parse output as JSON dict")


if __name__ == "__main__":
    demonstrate_task_parameters()
