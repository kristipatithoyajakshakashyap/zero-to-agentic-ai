"""
02_agents_deep_dive - Part 4: max_iter Parameter
================================================

Agents iterate: they reason, possibly call a tool, observe the result, and
reason again. max_iter caps this loop.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent_parameters import llm
from crewai import Agent, Task, Crew, Process


def demonstrate_max_iter():
    """Show how max_iter prevents infinite loops."""
    print("=" * 60)
    print("max_iter - Preventing Infinite Loops")
    print("=" * 60)

    iter_agent = Agent(
        role="Counter",
        goal="Count to 3, then stop.",
        backstory="You follow instructions precisely.",
        llm=llm,
        allow_delegation=False,
        max_iter=2,
        verbose=False,
    )

    iter_task = Task(
        description="Count from 1 to 3, listing each number on its own line.",
        expected_output="Three lines, one number each.",
        agent=iter_agent,
    )

    iter_crew = Crew(
        agents=[iter_agent],
        tasks=[iter_task],
        process=Process.sequential,
        verbose=False,
    )

    print("Agent with max_iter=2 (very low)")
    print("Task: Count from 1 to 3")
    print("\nRunning crew...")

    result = iter_crew.kickoff()
    print("Result (max_iter=2):", result.raw[:200])

    print("\nGuidelines for max_iter:")
    print("  - Too low (e.g. 1-2): agent may not finish simple tasks")
    print("  - Too high (e.g. 50): agent wastes time on hopeless tasks")
    print("  - Sweet spot: 5-15 for most tasks")
    print("  - Increase only if tools are slow or task is complex")
    print("  - Default is 15")


if __name__ == "__main__":
    demonstrate_max_iter()
