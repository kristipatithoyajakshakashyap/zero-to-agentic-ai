"""
05_research_assistant_crew - Part 2: Variant Without External Tools
=========================================================================

Sometimes you want the same researcher/writer/editor pipeline with no tools
at all - agents rely purely on the LLM's own knowledge. No API keys beyond
Groq are needed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from llm_setup import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process


def run_basic_crew():
    """Build and run the tool-free research/write/edit pipeline."""
    print("=" * 60)
    print("Research Assistant Crew (no tools, self-contained)")
    print("=" * 60)

    researcher_basic = Agent(
        role="Researcher",
        goal="Summarize key facts about AI agents.",
        backstory="You are a knowledgeable AI researcher.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    writer_basic = Agent(
        role="Writer",
        goal="Write a clear report from research notes.",
        backstory="You write accessible technical content.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    editor_basic = Agent(
        role="Editor",
        goal="Polish the report for clarity.",
        backstory="You are a careful editor.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    research_basic = Task(
        description=(
            "Based on your knowledge, summarize the current state of AI agent "
            "frameworks in 2026. Cover: CrewAI, AutoGen, LangGraph. List 3 "
            "key developments for each."
        ),
        expected_output="A structured summary with 3 points per framework.",
        agent=researcher_basic,
    )

    write_basic = Task(
        description=(
            "Write a 200-word comparison of the three major AI agent "
            "frameworks based on the research provided."
        ),
        expected_output="A concise comparison in markdown.",
        agent=writer_basic,
        context=[research_basic],
    )

    edit_basic = Task(
        description="Polish the comparison for grammar and flow.",
        expected_output="The final edited comparison.",
        agent=editor_basic,
        context=[write_basic],
    )

    basic_crew = Crew(
        agents=[researcher_basic, writer_basic, editor_basic],
        tasks=[research_basic, write_basic, edit_basic],
        process=Process.sequential,
        verbose=False,
    )

    basic_result = kickoff_with_retry(basic_crew)
    print("=== Basic Crew Result (no tools) ===")
    print(basic_result.raw[:500])
    return basic_result


if __name__ == "__main__":
    run_basic_crew()
