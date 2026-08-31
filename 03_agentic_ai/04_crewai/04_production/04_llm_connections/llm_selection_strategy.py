"""llm_selection_strategy -- a small "auto-pick the best provider" class,
plus a production LLM configuration checklist.

BEGINNER NOTES
--------------
In a real production system you rarely hardcode "always use Groq". Instead
you write a small strategy object that:
  1. Looks at which providers are actually available right now.
  2. Looks at what the task needs (is it a cheap/simple task, or a hard one?).
  3. Picks the provider that best matches those needs.

This file builds exactly that -- `LLMSelectionStrategy` -- scoped to the two
providers this course uses (Groq, Ollama). It ranks Groq above Ollama when
both are available (Groq is faster and higher quality), but happily falls
back to Ollama if Groq's key is missing or unreachable.

    python llm_selection_strategy.py
"""

from __future__ import annotations

import sys

from crewai import LLM

from provider_comparison import check_groq_reachable, check_ollama_reachable, GROQ_KEY

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LLMSelectionStrategy:
    """Picks the best reachable provider for a given task.

    Each provider is scored on quality and speed; the score is combined
    based on what the caller says they care about (`task_complexity`,
    `prefer_speed`). Providers that aren't actually reachable right now
    are never offered, so `select()` can never hand back a dead provider.
    """

    def __init__(self) -> None:
        self.providers: list[dict] = []

        # Groq: fast, high quality, needs a working API key.
        if check_groq_reachable():
            self.providers.append(
                {"name": "groq", "model": "groq/qwen/qwen3.8-27b", "quality_score": 8, "speed_score": 10}
            )

        # Ollama: local, always free, quality/speed depend on your hardware.
        if check_ollama_reachable():
            self.providers.append(
                {"name": "ollama", "model": "ollama/llama3.1:8b", "quality_score": 6, "speed_score": 5}
            )

    def select(self, task_complexity: str = "medium", prefer_speed: bool = False) -> LLM:
        """Return an LLM instance for the given task shape.

        Args:
            task_complexity: "low", "medium", or "high" -- higher complexity
                weighs quality more heavily.
            prefer_speed: if True, weighs speed more heavily than quality.
        """
        if not self.providers:
            raise RuntimeError(
                "No LLM provider is reachable. Set GROQ_API_KEY in "
                "03_agentic_ai/.env, or install and start Ollama."
            )

        scored = []
        for p in self.providers:
            if task_complexity == "high":
                score = p["quality_score"] * 2
            elif prefer_speed:
                score = p["speed_score"] * 2
            else:
                score = p["quality_score"] + p["speed_score"]
            scored.append((score, p))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        best = scored[0][1]
        base_model = best["model"].split("/", 1)[1] if best["name"] == "groq" else None
        if best["name"] == "groq":
            return LLM(model=best["model"], api_key=GROQ_KEY, temperature=0.7)
        return LLM(model=best["model"], base_url="http://localhost:11434", temperature=0.7)


PRODUCTION_CHECKLIST = [
    ("Primary provider", "Groq configured and tested"),
    ("Fallback provider", "Ollama configured for local failover"),
    ("API keys", "Loaded from .env, never hardcoded"),
    ("Temperature", "Set per agent (0 for analysis, 0.9 for creative)"),
    ("max_tokens", "Set to prevent runaway responses"),
    ("Rate limiting", "Retry/backoff around kickoff() calls (Groq free tier has TPM limits)"),
    ("Cost monitoring", "Track token usage per provider"),
    ("Latency logging", "Log response times for SLA compliance"),
]


if __name__ == "__main__":
    strategy = LLMSelectionStrategy()
    print("=== LLMSelection Strategy ===")
    print(f"Reachable providers: {[p['name'] for p in strategy.providers]}\n")

    for complexity in ["low", "medium", "high"]:
        llm = strategy.select(task_complexity=complexity)
        print(f"  Task complexity={complexity:8s} -> {llm.model}")

    llm = strategy.select(task_complexity="medium", prefer_speed=True)
    print(f"  Speed preference   -> {llm.model}")

    print("\n=== Production LLM Configuration Checklist ===")
    for item, detail in PRODUCTION_CHECKLIST:
        print(f"  [x] {item:20s} -- {detail}")
