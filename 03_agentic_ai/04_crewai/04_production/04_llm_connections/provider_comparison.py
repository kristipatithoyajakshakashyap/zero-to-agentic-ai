"""provider_comparison -- compare the two LLM providers this course uses:
Groq (fast cloud inference) and Ollama (free local inference).

BEGINNER NOTES
--------------
CrewAI does not talk to an LLM provider directly. Under the hood it uses a
library called LiteLLM, which understands a single naming convention for
"which provider + which model" you want:

    "<provider>/<model_name>"

Examples: "groq/qwen/qwen3.8-27b", "ollama/llama3.1:8b".

This course uses exactly two providers, in this priority order:
1. Groq   -- a cloud service. Very fast. Needs a free API key (GROQ_API_KEY
             in 03_agentic_ai/.env). Get one at https://console.groq.com.
2. Ollama -- runs entirely on your own machine. No key needed, but you must
             have Ollama installed and a model pulled (`ollama pull llama3.1:8b`).

We never use OpenAI in this course -- CrewAI supports it, but this course is
Groq-first by design, so every helper below only tries Groq then Ollama.

    python provider_comparison.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from crewai import LLM
from dotenv import load_dotenv

# Windows terminals default to a limited text encoding (cp1252) that cannot
# print every character an LLM might return (e.g. curly quotes, em dashes).
# Reconfiguring stdout to UTF-8 avoids crashes on those characters.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _find_track() -> Path:
    """Walk up the folder tree until we reach the 03_agentic_ai directory,
    which is where the shared .env file (with API keys) lives. This lets
    every script in the course be run from any working directory."""
    p = Path(__file__).resolve()
    while p.name != "03_agentic_ai" and p.parent != p:
        p = p.parent
    return p


TRACK = _find_track()
load_dotenv(TRACK / ".env", override=False)

# Read the two keys/flags we care about so we can print a clear status
# report before doing anything else -- this is good practice for any
# script that depends on external services.
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")


def check_groq_reachable() -> bool:
    """Ping Groq's models endpoint to confirm the API key actually works
    (not just that it's present in .env)."""
    if not GROQ_KEY:
        return False
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            timeout=5,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def check_ollama_reachable() -> bool:
    """Ping the local Ollama server. Returns False (not an exception) if
    Ollama isn't installed or isn't running -- callers use this to decide
    whether to offer Ollama as a fallback."""
    try:
        return requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200
    except requests.RequestException:
        return False


def get_groq_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.7) -> LLM:
    """Build an LLM object pointed at Groq. Raises if Groq isn't reachable
    so the caller finds out immediately instead of silently failing later."""
    if not check_groq_reachable():
        raise RuntimeError("Groq is not reachable. Check GROQ_API_KEY in 03_agentic_ai/.env.")
    return LLM(model=f"groq/{model}", api_key=GROQ_KEY, temperature=temperature)


def get_ollama_llm(temperature: float = 0.7) -> LLM:
    """Build an LLM object pointed at a local Ollama server."""
    return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature)


# A quick side-by-side reference table students can scan without running
# any code -- this is the kind of thing you'd pin above your desk.
COMPARISON_TABLE = [
    ("Cost", "Free tier + paid", "Free (your own hardware)"),
    ("Speed", "Very fast (specialized inference hardware)", "Depends on your CPU/GPU"),
    ("Quality", "Great -- open models like Llama, Qwen", "Good -- smaller local models"),
    ("Privacy", "Cloud (data leaves your machine)", "Fully local"),
    ("Setup", "Just an API key", "Install Ollama + pull a model"),
    ("Model string", "groq/<model-name>", "ollama/<model-name>"),
]


if __name__ == "__main__":
    print("=== 1. Which providers are actually reachable right now? ===")
    groq_ok = check_groq_reachable()
    ollama_ok = check_ollama_reachable()
    print(f"  Groq (GROQ_API_KEY):  {'REACHABLE' if groq_ok else 'not reachable'}")
    print(f"  Ollama (local):       {'REACHABLE' if ollama_ok else 'not reachable'}")

    print("\n=== 2. Side-by-side comparison ===")
    print(f"{'Feature':12s} {'Groq':45s} {'Ollama':30s}")
    print("-" * 90)
    for feature, groq_val, ollama_val in COMPARISON_TABLE:
        print(f"{feature:12s} {groq_val:45s} {ollama_val:30s}")

    print("\n=== 3. Live call to whichever provider is reachable ===")
    if groq_ok:
        llm = get_groq_llm()
        print(f"Using Groq ({llm.model}). Response: {llm.call('Reply with exactly 3 words: Groq is fast')}")
    elif ollama_ok:
        llm = get_ollama_llm()
        print(f"Using Ollama ({llm.model}). Response: {llm.call('Reply with exactly 3 words: Ollama runs locally')}")
    else:
        raise RuntimeError(
            "Neither Groq nor Ollama is reachable. Set GROQ_API_KEY in "
            "03_agentic_ai/.env, or install and start Ollama."
        )

    print("\n=== 4. Temperature and max_tokens presets ===")
    print("Temperature controls randomness: 0 = deterministic/repeatable, 1 = creative.")
    print("max_tokens caps how long the reply can be (protects against runaway cost/latency).")
    presets = {
        "analysis": {"temperature": 0.0, "max_tokens": 1000, "use_case": "Data analysis, extraction, classification"},
        "creative": {"temperature": 0.9, "max_tokens": 2000, "use_case": "Writing, brainstorming"},
        "code": {"temperature": 0.2, "max_tokens": 3000, "use_case": "Code generation, debugging"},
        "quick": {"temperature": 0.0, "max_tokens": 100, "use_case": "Fast classification/routing"},
    }
    for name, cfg in presets.items():
        print(f"  {name:10s}: temperature={cfg['temperature']}, max_tokens={cfg['max_tokens']:5d} -- {cfg['use_case']}")
