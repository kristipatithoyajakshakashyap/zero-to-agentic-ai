"""
03_tasks_and_processes - Part 2: Sequential vs Hierarchical Processes
======================================================================

Process.sequential vs Process.hierarchical - when to use each.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process


def demonstrate_sequential():
    """Show sequential process - tasks run in order with context passing."""
    print("=" * 60)
    print("Sequential Process")
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

    editor = Agent(
        role="Editor",
        goal="Polish the blog post for clarity and grammar.",
        backstory="You are a meticulous editor.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    plan_task = Task(
        description="Create a 3-point outline for a blog post about Python decorators.",
        expected_output="A numbered outline with 3 main points.",
        agent=planner,
    )

    write_task = Task(
        description="Write a short blog post (150-200 words) following the outline.",
        expected_output="A complete blog post in markdown format.",
        agent=writer,
        context=[plan_task],
    )

    edit_task = Task(
        description="Polish the blog post: fix grammar, improve flow, tighten prose.",
        expected_output="The final edited version of the blog post.",
        agent=editor,
        context=[write_task],
    )

    sequential_crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan_task, write_task, edit_task],
        process=Process.sequential,
        verbose=False,
    )

    print("Sequential crew:", len(sequential_crew.agents), "agents,", len(sequential_crew.tasks), "tasks")
    print("Process: Tasks run in order, each receiving prior outputs via context")

    seq_result = kickoff_with_retry(sequential_crew)
    print("\n=== Final Blog Post ===")
    print(seq_result.raw)


def demonstrate_hierarchical():
    """Show hierarchical process - manager agent delegates automatically."""
    print("\n" + "=" * 60)
    print("Hierarchical Process")
    print("=" * 60)

    analyst = Agent(
        role="Market Analyst",
        goal="Analyze market trends with data.",
        backstory="You are a data-driven market analyst.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    strategist = Agent(
        role="Strategist",
        goal="Turn analysis into actionable recommendations.",
        backstory="You translate data into strategy.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    hier_task = Task(
        description=(
            "Analyze the rise of edge AI in 2025-2026 and recommend "
            "three strategic actions for a tech startup."
        ),
        expected_output="Market analysis followed by 3 recommendations.",
        agent=analyst,
    )

    def build_hier_crew():
        return Crew(
            agents=[analyst, strategist],
            tasks=[hier_task],
            process=Process.hierarchical,
            manager_llm=llm,
            verbose=False,
        )

    print("Hierarchical crew: 2 agents (manager auto-created by CrewAI).")
    print("Process: Manager agent auto-delegates to specialists")

    hier_result = kickoff_with_retry(build_hier_crew)
    print("\n=== Hierarchical Result ===")
    print(hier_result.raw[:500])

    print("\nWhen to use each:")
    print("  Sequential: Predictable workflows, known task order, context chaining")
    print("  Hierarchical: Complex routing, content-dependent delegation, supervisory layer")
    print("  Note: Hierarchical adds overhead from extra LLM calls")


if __name__ == "__main__":
    demonstrate_sequential()
    demonstrate_hierarchical()
