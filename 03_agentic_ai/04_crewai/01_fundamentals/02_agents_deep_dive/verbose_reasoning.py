"""
02_agents_deep_dive - Part 5: Verbose vs Reasoning
===================================================

Debugging output modes for agents.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent_parameters import llm
from crewai import Agent, Task, Crew, Process


def demonstrate_verbose_reasoning():
    """Show verbose vs reasoning output modes."""
    print("=" * 60)
    print("Verbose vs Reasoning - Debugging Output")
    print("=" * 60)

    verbose_agent = Agent(
        role="Echo",
        goal="Repeat back what you were told.",
        backstory="You repeat things.",
        llm=llm,
        allow_delegation=False,
        verbose=True,
        reasoning=False,
    )

    echo_task = Task(
        description="Say: 'The quick brown fox jumps over the lazy dog.'",
        expected_output="The exact sentence quoted above.",
        agent=verbose_agent,
    )

    echo_crew = Crew(
        agents=[verbose_agent],
        tasks=[echo_task],
        process=Process.sequential,
        verbose=True,
    )

    print("Running with verbose=True, reasoning=False...")
    print("(Shows agent/task start/end, tool calls, final output)")
    echo_result = echo_crew.kickoff()
    print("\nFinal output:", echo_result.raw)

    print("\nComparison:")
    print("  verbose=True  : Agent/task start/end, tool calls, final output")
    print("  reasoning=True: Full chain-of-thought thought process at each step")
    print("\nRecommendations:")
    print("  - Development: verbose=True to see execution flow")
    print("  - Debugging decisions: reasoning=True to understand why")
    print("  - Production: Both False for clean output")


if __name__ == "__main__":
    demonstrate_verbose_reasoning()
