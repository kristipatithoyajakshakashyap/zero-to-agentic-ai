"""
03_tasks_and_processes - Part 7: Batch Execution with kickoff_for_each
========================================================================

crew.kickoff_for_each(inputs=[...]) runs the same crew multiple times, once
per input dict. Each input is interpolated into task descriptions using
{key} placeholders - useful for processing a list of items through the
same agent pipeline.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm
from crewai import Agent, Task, Crew, Process


def demonstrate_batch_kickoff_for_each():
    """Process three topics through the same plan-write pipeline."""
    print("=" * 60)
    print("Batch Execution - kickoff_for_each")
    print("=" * 60)

    batch_planner = Agent(
        role="Batch Planner",
        goal="Create an outline for the given topic.",
        backstory="You plan technical content efficiently.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    batch_writer = Agent(
        role="Batch Writer",
        goal="Write a short explanation from the outline.",
        backstory="You write concise technical content.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    # {topic} placeholder in the description - kickoff_for_each fills it.
    batch_plan = Task(
        description="Create a 2-point outline explaining {topic}.",
        expected_output="A numbered outline with 2 points.",
        agent=batch_planner,
    )

    batch_write = Task(
        description="Write a 2-3 sentence explanation of {topic} following the outline.",
        expected_output="A short explanation paragraph.",
        agent=batch_writer,
        context=[batch_plan],
    )

    batch_crew = Crew(
        agents=[batch_planner, batch_writer],
        tasks=[batch_plan, batch_write],
        process=Process.sequential,
        verbose=False,
    )

    topics = [
        {"topic": "Python decorators"},
        {"topic": "list comprehensions"},
        {"topic": "context managers"},
    ]

    batch_results = batch_crew.kickoff_for_each(inputs=topics)
    for i, res in enumerate(batch_results):
        print(f"\n=== Topic {i + 1}: {topics[i]['topic']} ===")
        print(res.raw[:300])

    print("\nKey point:")
    print("  - kickoff_for_each(inputs=[...]) reruns the whole crew per input dict")
    print("  - {key} placeholders in task descriptions get interpolated per run")


if __name__ == "__main__":
    demonstrate_batch_kickoff_for_each()
