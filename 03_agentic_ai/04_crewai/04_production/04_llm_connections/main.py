"""main -- run the full llm_connections module end to end.

    python main.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from provider_comparison import COMPARISON_TABLE, check_groq_reachable, check_ollama_reachable, get_groq_llm, get_ollama_llm
from llm_selection_strategy import PRODUCTION_CHECKLIST, LLMSelectionStrategy


def main() -> None:
    print("=== 1. Provider reachability + comparison ===")
    groq_ok = check_groq_reachable()
    ollama_ok = check_ollama_reachable()
    print(f"  Groq: {'REACHABLE' if groq_ok else 'not reachable'}, Ollama: {'REACHABLE' if ollama_ok else 'not reachable'}")
    for feature, groq_val, ollama_val in COMPARISON_TABLE:
        print(f"  {feature:12s} Groq: {groq_val:45s} Ollama: {ollama_val}")

    print("\n=== 2. Live call ===")
    llm = get_groq_llm() if groq_ok else get_ollama_llm()
    print(f"Using {llm.model}: {llm.call('Reply with exactly 3 words.')}")

    print("\n=== 3. LLMSelection strategy + checklist ===")
    strategy = LLMSelectionStrategy()
    for complexity in ["low", "high"]:
        picked = strategy.select(task_complexity=complexity)
        print(f"  complexity={complexity} -> {picked.model}")
    for item, detail in PRODUCTION_CHECKLIST:
        print(f"  [x] {item:20s} -- {detail}")


if __name__ == "__main__":
    main()
