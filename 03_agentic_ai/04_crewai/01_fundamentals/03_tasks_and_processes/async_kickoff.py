"""
03_tasks_and_processes - Part 6: Async Kickoff
===============================================

Running crews asynchronously with kickoff_async().
"""

import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm
from crewai import Agent, Task, Crew, Process


async def run_crew_async():
    """Run a simple crew asynchronously."""
    async_agent = Agent(
        role="Async Responder",
        goal="Reply quickly with a fact.",
        backstory="You are fast.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    async_task = Task(
        description="Name one fact about the Python programming language.",
        expected_output="A single factual statement.",
        agent=async_agent,
    )

    async_crew = Crew(
        agents=[async_agent],
        tasks=[async_task],
        process=Process.sequential,
        verbose=False,
    )

    result = await async_crew.kickoff_async()
    return result


def demonstrate_async_kickoff():
    """Show async crew execution."""
    print("=" * 60)
    print("Async Kickoff")
    print("=" * 60)

    print("Running crew asynchronously with await crew.kickoff_async()...")
    async_result = asyncio.run(run_crew_async())
    print("Async result:", async_result.raw)

    print("\nKey points:")
    print("  - crew.kickoff_async() returns a coroutine")
    print("  - Use await in async contexts (FastAPI, async Jupyter)")
    print("  - CrewAI runs internal LLM calls in threads")
    print("  - Crew itself is still single-threaded (tasks run sequentially)")


if __name__ == "__main__":
    demonstrate_async_kickoff()
