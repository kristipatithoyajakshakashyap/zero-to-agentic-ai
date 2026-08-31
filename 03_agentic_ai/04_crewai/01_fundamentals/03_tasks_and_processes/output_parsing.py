"""
03_tasks_and_processes - Part 5: Output Parsing
================================================

CrewOutput access patterns: raw, pydantic, json_dict, token_usage.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from task_basics import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process


def demonstrate_output_parsing():
    """Show multiple access patterns for CrewOutput."""
    print("=" * 60)
    print("Output Parsing")
    print("=" * 60)

    parse_task = Task(
        description="Name the three primary colors and explain why they are primary.",
        expected_output="A list of 3 colors with one-sentence explanations.",
        agent=Agent(
            role="Art Teacher",
            goal="Explain color theory basics.",
            backstory="You teach foundational art concepts.",
            llm=llm,
            allow_delegation=False,
            verbose=False,
        ),
    )

    parse_crew = Crew(
        agents=[parse_task.agent],
        tasks=[parse_task],
        process=Process.sequential,
        verbose=False,
    )

    parse_result = kickoff_with_retry(parse_crew)
    print("=== Raw Output ===")
    print(parse_result.raw)
    print("\n=== Token Usage ===")
    print("  prompt_tokens    :", parse_result.token_usage.prompt_tokens)
    print("  completion_tokens:", parse_result.token_usage.completion_tokens)
    print("  total_tokens     :", parse_result.token_usage.total_tokens)

    print("\nCrewOutput Access Patterns:")
    print("  .raw         : Plain string from the last task (always available)")
    print("  .pydantic    : Pydantic model instance (if output_pydantic set on task)")
    print("  .json_dict   : Python dict (if output_json=True set on task)")
    print("  .token_usage : Token counts for the run")
    print("  .tasks_output: List of individual task outputs")


if __name__ == "__main__":
    demonstrate_output_parsing()
