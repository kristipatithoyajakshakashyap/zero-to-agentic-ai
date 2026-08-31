"""Module 02 - Knowledge Sources: run every section in sequence.

Run: python main.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from agent_vs_crew_knowledge import demonstrate_agent_vs_crew_knowledge
from direct_retrieval import demonstrate_direct_retrieval
from pdf_knowledge_source import demonstrate_pdf_knowledge_source
from text_knowledge_source import demonstrate_text_knowledge_source


def main() -> None:
    print("\n--- 1. Text file knowledge source ---")
    demonstrate_text_knowledge_source()

    print("\n--- 2. PDF knowledge source ---")
    demonstrate_pdf_knowledge_source()

    print("\n--- 3. Agent-scoped vs crew-shared knowledge ---")
    demonstrate_agent_vs_crew_knowledge()

    print("\n--- 4. Direct retrieval without a crew ---")
    demonstrate_direct_retrieval()


if __name__ == "__main__":
    main()
