"""
02_agents_deep_dive - Part 3: Delegation
=========================================

When allow_delegation=True (the default), an agent can hand off sub-tasks to
other agents in the crew. This is CrewAI's built-in hierarchical pattern.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent_parameters import llm
from crewai import Agent, Task, Crew, Process


def demonstrate_delegation():
    """Show agent-to-agent handoff with allow_delegation."""
    print("=" * 60)
    print("Agent Delegation (allow_delegation)")
    print("=" * 60)

    delegator = Agent(
        role="Project Manager",
        goal="Coordinate the team to complete the task.",
        backstory="You delegate effectively to specialists.",
        llm=llm,
        allow_delegation=True,
        verbose=False,
    )

    specialist = Agent(
        role="Data Analyst",
        goal="Analyze data and report findings.",
        backstory="You are a careful data analyst.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    deleg_task = Task(
        description="Analyze the trend: AI funding grew 40 percent in 2025.",
        expected_output="A 2-3 sentence analysis of the trend.",
        agent=delegator,
    )

    deleg_crew = Crew(
        agents=[delegator, specialist],
        tasks=[deleg_task],
        process=Process.sequential,
        verbose=False,
    )

    print("Delegator:", delegator.role, "(allow_delegation=True)")
    print("Specialist:", specialist.role, "(allow_delegation=False)")
    print("\nRunning crew with delegation...")

    deleg_result = deleg_crew.kickoff()
    print("Delegation result:", deleg_result.raw[:300])

    print("\nKey points:")
    print("  - allow_delegation=True enables agent-to-agent handoff")
    print("  - Adds latency (extra LLM calls)")
    print("  - Only enable when workflow genuinely needs agent communication")
    print("  - Use for manager/coordinator agents that orchestrate others")


if __name__ == "__main__":
    demonstrate_delegation()
