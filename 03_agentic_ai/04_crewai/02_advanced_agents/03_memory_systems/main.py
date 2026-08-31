"""Module 03 - Memory Systems: run every section in sequence.

Run: python main.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from combined_memory_demo import demonstrate_combined_memory
from entity_memory import demonstrate_entity_memory
from long_term_memory import demonstrate_long_term_memory
from short_term_memory import demonstrate_short_term_memory


def main() -> None:
    print("\n--- 1. Short-term memory (task context chaining) ---")
    demonstrate_short_term_memory()

    print("\n--- 2. Long-term memory (SQLite persistence) ---")
    demonstrate_long_term_memory()

    print("\n--- 3. Entity memory (entity table) ---")
    demonstrate_entity_memory()

    print("\n--- 4. Combined memory ---")
    demonstrate_combined_memory()


if __name__ == "__main__":
    main()
