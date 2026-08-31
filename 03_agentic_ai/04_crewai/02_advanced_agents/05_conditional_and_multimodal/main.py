"""Module 05 - Conditional and Multimodal: run every section in sequence.

Run: python main.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from conditional_tasks import demonstrate_conditional_tasks
from multimodal_vision_agent import demonstrate_multimodal_vision


def main() -> None:
    print("\n--- 1. Conditional task branching ---")
    demonstrate_conditional_tasks()

    print("\n--- 2. Multimodal vision agent ---")
    demonstrate_multimodal_vision()


if __name__ == "__main__":
    main()
