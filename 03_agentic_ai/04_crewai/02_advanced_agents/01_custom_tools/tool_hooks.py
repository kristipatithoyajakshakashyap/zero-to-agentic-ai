"""Module 01 - Custom Tools: pre/post call hooks around tool execution.

BEGINNER NOTE: In production you often want to log, time, or audit
every tool call an agent makes — useful for debugging and cost
tracking. This lesson shows the pattern by hand: wrap tool.run() with
a "before" and "after" logging function. (CrewAI's built-in event
system, covered in the production/observability module, does this more
formally — this is the simple manual version.)

Run standalone: python tool_hooks.py
"""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import time

from crewai.tools import tool

_call_log: list[str] = []


def before_call(tool_name: str, **kwargs) -> None:
    _call_log.append(f"[before] {tool_name} args={kwargs}")


def after_call(tool_name: str, result: str, duration: float) -> None:
    _call_log.append(f"[after]  {tool_name} -> {result!r} ({duration:.4f}s)")


@tool("Uppercase Text")
def uppercase_text(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


def run_with_hooks(tool_obj, **kwargs) -> str:
    before_call(tool_obj.name, **kwargs)
    start = time.perf_counter()
    result = tool_obj.run(**kwargs)
    duration = time.perf_counter() - start
    after_call(tool_obj.name, result, duration)
    return result


def demonstrate_tool_hooks() -> None:
    run_with_hooks(uppercase_text, text="groq is fast")
    for entry in _call_log:
        print(entry)


if __name__ == "__main__":
    demonstrate_tool_hooks()
