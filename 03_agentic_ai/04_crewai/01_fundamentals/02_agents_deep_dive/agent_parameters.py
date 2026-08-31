"""
02_agents_deep_dive - Part 1: Agent Parameters
================================================
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


from crewai import LLM, Agent

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

resp = llm.call("Reply with just the word OK.")
print("[OK] LLM live, responded:", resp[:40])


def demonstrate_core_parameters():
    """Demonstrate the six core Agent parameters."""
    print("\n" + "=" * 60)
    print("Core Agent Parameters")
    print("=" * 60)

    researcher = Agent(
        role="Senior Research Analyst",
        goal="Uncover cutting-edge developments in AI.",
        backstory=(
            "You are a veteran researcher at a top tech think tank. "
            "Your expertise lies in identifying emerging trends."
        ),
        llm=llm,
        tools=[],
        allow_delegation=False,
        max_iter=5,
        verbose=True,
        reasoning=False,
    )

    print("Agent created:", researcher.role)
    print("  max_iter        :", researcher.max_iter)
    print("  allow_delegation:", researcher.allow_delegation)
    print("  verbose         :", researcher.verbose)

    print("\nParameter Reference:")
    print("  role             : Short title for the agent")
    print("  goal             : One-sentence objective")
    print("  backstory        : Context paragraph that shapes LLM persona")
    print("  llm              : The language model powering this agent")
    print("  tools            : Tool objects the agent can call")
    print("  allow_delegation : Can this agent hand tasks to other agents?")
    print("  max_iter         : Max reasoning iterations before forced stop")
    print("  verbose          : Print detailed execution logs")
    print("  reasoning        : Enable explicit chain-of-thought logging")


if __name__ == "__main__":
    demonstrate_core_parameters()
