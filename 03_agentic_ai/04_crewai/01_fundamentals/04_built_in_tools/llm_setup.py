"""
04_built_in_tools - Shared LLM setup
=====================================

Defines get_llm(), llm, and kickoff_with_retry() used by every file in this
module. Not a cross-module common file - lives inside this module only, and
every other file in this module imports it (same pattern as prior modules).
"""

import os
import sys
import time
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

from crewai import LLM, Crew

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"


def get_llm(model: str | None = None, temperature: float = 0.0, **kw) -> LLM:
    """Groq-first LLM resolver. Falls back to local Ollama only - no OpenAI.

    Every CrewAI Agent needs an `llm` to think with. Rather than hardcoding
    one provider, this function checks what's actually available at runtime:
      1. Try Groq first (fast, cloud-hosted, needs GROQ_API_KEY in .env).
      2. If Groq is unreachable, try a locally-running Ollama server instead.
      3. If neither works, fail loudly with a clear fix-it message - we never
         want a crew to silently run against the wrong model.
    `crewai.LLM` is CrewAI's own wrapper (built on LiteLLM) that understands
    the "provider/model-name" string format, e.g. "groq/qwen/qwen3.8-27b".
    """
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            # A lightweight GET to Groq's /models endpoint just proves the
            # key is valid and Groq is reachable - it costs no LLM tokens.
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass  # Network hiccup or Groq down - fall through to Ollama.

    try:
        # Ollama exposes a local REST API; /api/tags lists installed models
        # and is a cheap way to check "is a local server even running?".
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kw)
    except requests.RequestException:
        pass

    # Neither provider worked - raise instead of returning something broken,
    # so failures show up immediately instead of deep inside a crew run.
    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


llm = get_llm()

resp = llm.call("Reply OK")
print("[OK] LLM live:", resp[:30])


def kickoff_with_retry(crew_or_factory, max_retries: int = 4, base_delay: float = 65.0, **kickoff_kw):
    """Run crew.kickoff(), retrying on Groq's free-tier rate limit (429).

    Accepts either a ready-built Crew or a zero-arg factory that builds a
    fresh Crew each attempt (needed for crews whose kickoff() mutates state).
    """
    build = crew_or_factory if callable(crew_or_factory) and not isinstance(crew_or_factory, Crew) else (lambda: crew_or_factory)

    for attempt in range(1, max_retries + 1):
        crew = build()
        try:
            return crew.kickoff(**kickoff_kw)
        except Exception as exc:  # noqa: BLE001
            if "rate_limit" in str(exc).lower() or "429" in str(exc):
                if attempt == max_retries:
                    raise
                print(f"[RATE LIMIT] Waiting {base_delay:.0f}s before retry {attempt}/{max_retries}...")
                time.sleep(base_delay)
                continue
            raise


if __name__ == "__main__":
    print("LLM resolver ready. Model:", llm.model)
