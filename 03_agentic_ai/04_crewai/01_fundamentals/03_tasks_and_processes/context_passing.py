"""
03_tasks_and_processes - Part 3: Context Passing
================================================

How task outputs chain together via the context parameter.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process


def demonstrate_context_passing():
    """Show how context passes data between tasks."""
    print("=" * 60)
    print("Context Passing Between Tasks")
    print("=" * 60)

    planner = Agent(
        role="Planner",
        goal="Create a brief plan for a blog post.",
        backstory="You are a content strategist.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    writer = Agent(
        role="Writer",
        goal="Write the blog post based on the plan.",
        backstory="You are a skilled content writer.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    research_task = Task(
        description="Research the top 3 Python web frameworks in 2026.",
        expected_output="A list of 3 frameworks with one-sentence descriptions.",
        agent=planner,
    )

    summary_task = Task(
        description="Write a comparison table of the 3 frameworks.",
        expected_output="A markdown table with framework name, pros, and cons.",
        agent=writer,
        context=[research_task],
    )

    context_crew = Crew(
        agents=[planner, writer],
        tasks=[research_task, summary_task],
        process=Process.sequential,
        verbose=False,
    )

    print("Task 1: Research top 3 Python web frameworks")
    print("Task 2: Write comparison table (receives Task 1 output via context)")
    print()

    ctx_result = kickoff_with_retry(context_crew)
    print("\n=== Context-Passed Result ===")
    print(ctx_result.raw[:500])

    print("\nKey point:")
    print("  - context=[prior_task] injects prior task output into agent's prompt")
    print("  - Without context, each task runs in isolation")
    print("  - This is how information flows from one task to the next")


if __name__ == "__main__":
    demonstrate_context_passing()
