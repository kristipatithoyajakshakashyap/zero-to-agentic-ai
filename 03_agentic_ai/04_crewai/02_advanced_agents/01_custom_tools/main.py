"""Module 01 - Custom Tools: run every section in sequence.

Run: python main.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from agent_with_custom_tools import demonstrate_agent_with_custom_tools
from base_tool_subclass import demonstrate_base_tool_subclass
from tool_decorator_basics import demonstrate_tool_decorator
from tool_error_handling import demonstrate_tool_error_handling
from tool_hooks import demonstrate_tool_hooks


def main() -> None:
    print("\n--- 1. @tool decorator basics ---")
    demonstrate_tool_decorator()

    print("\n--- 2. BaseTool subclass ---")
    demonstrate_base_tool_subclass()

    print("\n--- 3. Error handling ---")
    demonstrate_tool_error_handling()

    print("\n--- 4. Tool hooks ---")
    demonstrate_tool_hooks()

    print("\n--- 5. Agent with custom tools (live crew run) ---")
    demonstrate_agent_with_custom_tools()


if __name__ == "__main__":
    main()
