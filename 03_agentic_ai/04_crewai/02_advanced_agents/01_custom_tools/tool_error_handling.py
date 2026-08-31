"""Module 01 - Custom Tools: error handling and graceful degradation.

BEGINNER NOTE: An agent only sees a tool's *return value*, not a Python
traceback. If your tool code raises an exception, the agent gets a
confusing failure it can't reason about. Best practice: catch expected
errors inside the tool and return a clear, readable error string
instead — the LLM can read that and decide what to do next (retry,
ask for different input, etc.).

Run standalone: python tool_error_handling.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai.tools import tool


@tool("Safe Divider")
def safe_divide(numerator: float, denominator: float) -> str:
    """Divide two numbers, returning a readable error instead of raising."""
    try:
        return str(numerator / denominator)
    except ZeroDivisionError:
        return "Error: cannot divide by zero. Please provide a non-zero denominator."


@tool("Safe JSON Field")
def safe_get_field(payload: dict, field: str) -> str:
    """Look up a field in a dict, returning a clear message if missing."""
    if field in payload:
        return str(payload[field])
    return f"Error: field '{field}' not found. Available fields: {list(payload.keys())}"


def demonstrate_tool_error_handling() -> None:
    print(safe_divide.run(numerator=10, denominator=2))
    print(safe_divide.run(numerator=10, denominator=0))
    print(safe_get_field.run(payload={"name": "crew"}, field="name"))
    print(safe_get_field.run(payload={"name": "crew"}, field="missing"))


if __name__ == "__main__":
    demonstrate_tool_error_handling()
