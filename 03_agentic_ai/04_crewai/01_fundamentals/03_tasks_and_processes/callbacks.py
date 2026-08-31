"""
03_tasks_and_processes - Part 4: Callback Functions
====================================================

Callback functions for post-task processing.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process


def demonstrate_callbacks():
    """Show callback functions for task completion hooks."""
    print("=" * 60)
    print("Callback Functions")
    print("=" * 60)

    callback_log = []

    def log_callback(output):
        """Append task info to the log and print a confirmation."""
        callback_log.append({
            "role": output.pydantic.__dict__ if output.pydantic else None,
            "raw_length": len(output.raw),
        })
        print("[callback] Task finished. Raw output length:", len(output.raw))

    cb_agent = Agent(
        role="Poet",
        goal="Write a haiku.",
        backstory="You are a master of Japanese poetry.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    cb_task = Task(
        description="Write a haiku about machine learning.",
        expected_output="Three lines in 5-7-5 syllable format.",
        agent=cb_agent,
        callback=log_callback,
    )

    cb_crew = Crew(
        agents=[cb_agent],
        tasks=[cb_task],
        process=Process.sequential,
        verbose=False,
    )

    print("Task with callback: Write a haiku about machine learning")
    print("Callback logs: task completion, output length")
    print()

    cb_result = kickoff_with_retry(cb_crew)
    print("\n=== Haiku ===")
    print(cb_result.raw)
    print("\nCallback log:", callback_log)

    print("\nUse cases for callbacks:")
    print("  - Logging results to a database")
    print("  - Triggering downstream pipelines")
    print("  - Saving output to disk")
    print("  - Validating output before proceeding")
    print("  - Callbacks run AFTER task completes but BEFORE next task starts")


if __name__ == "__main__":
    demonstrate_callbacks()
