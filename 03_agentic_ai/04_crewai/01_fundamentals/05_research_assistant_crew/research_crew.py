"""
05_research_assistant_crew - Part 1: Full Crew (Researcher, Writer, Editor)
================================================================================

A complete multi-agent crew: researcher reads a reference file and scrapes
the web, writer turns findings into a report, editor polishes it. Three
agents, three tasks chained via context, one sequential process.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from llm_setup import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, ScrapeWebsiteTool

DATA_DIR = Path.cwd() / "_research_demo"


def setup_reference_file() -> Path:
    """Create the sample reference file the researcher agent will read."""
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    DATA_DIR.mkdir(parents=True)

    reference_file = DATA_DIR / "reference_notes.txt"
    reference_file.write_text(
        "Research Notes: AI Agents in 2026\n"
        "==================================\n"
        "\n"
        "1. Multi-agent frameworks like CrewAI, AutoGen, and LangGraph have\n"
        "   matured significantly. CrewAI focuses on role-based collaboration\n"
        "   with a simple Agent-Task-Crew abstraction.\n"
        "\n"
        "2. Key trend: agents are moving from demos to production. Companies\n"
        "   are deploying customer support agents, code review agents, and\n"
        "   research assistants at scale.\n"
        "\n"
        "3. Tool integration has become standardized. Agents can use web search,\n"
        "   file I/O, database queries, and API calls through unified tool\n"
        "   interfaces.\n"
        "\n"
        "4. The main challenges are: reliability (hallucination prevention),\n"
        "   cost control (token usage), and observability (logging agent\n"
        "   decisions for debugging).\n"
        "\n"
        "5. Open-source models (Llama 3.2, Mistral, Qwen) are now competitive\n"
        "   with proprietary models for many agent tasks, enabling fully\n"
        "   local and private deployments.\n"
    )
    print("Reference file created:", reference_file)
    print("Contents:\n", reference_file.read_text()[:200], "...")
    return reference_file


def build_agents() -> tuple[Agent, Agent, Agent]:
    """Define the three specialized agents: researcher, writer, editor."""
    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            "Gather comprehensive, accurate information on the given topic "
            "from reference materials and web sources."
        ),
        backstory=(
            "You are a seasoned research analyst with expertise in AI and "
            "technology. You are meticulous about sourcing and always cite "
            "your references. You read files carefully and extract key facts."
        ),
        llm=llm,
        tools=[FileReadTool(), ScrapeWebsiteTool()],
        allow_delegation=False,
        max_iter=8,
        verbose=True,
    )

    writer = Agent(
        role="Technical Writer",
        goal=(
            "Transform raw research findings into a well-structured, "
            "engaging report that is clear and accessible."
        ),
        backstory=(
            "You are a skilled technical writer who excels at turning complex "
            "topics into readable content. You use clear headings, short "
            "paragraphs, and concrete examples."
        ),
        llm=llm,
        tools=[],
        allow_delegation=False,
        max_iter=5,
        verbose=True,
    )

    editor = Agent(
        role="Senior Editor",
        goal=(
            "Polish the report for grammar, clarity, flow, and conciseness. "
            "Ensure the final output is publication-ready."
        ),
        backstory=(
            "You are a meticulous editor with decades of experience in "
            "technical publishing. You catch awkward phrasing, fix grammar, "
            "and tighten prose without losing meaning."
        ),
        llm=llm,
        tools=[],
        allow_delegation=False,
        max_iter=3,
        verbose=True,
    )

    print("All 3 agents defined:", researcher.role, "|", writer.role, "|", editor.role)
    return researcher, writer, editor


def build_tasks(researcher: Agent, writer: Agent, editor: Agent, reference_file: Path) -> tuple[Task, Task, Task]:
    """Define the three tasks, chained via context: research -> write -> edit.

    `context=[research_task]` on write_task is the important part: CrewAI
    passes research_task's output as extra input into write_task's prompt,
    so the writer agent "sees" what the researcher found without you having
    to manually copy text between steps. Same pattern chains write -> edit.
    """
    research_task = Task(
        description=(
            f"Read the reference file at {reference_file} and summarize the "
            "key findings about AI agents in 2026. Organize the summary into "
            "3-5 bullet points covering: frameworks, production adoption, tool "
            "integration, challenges, and open-source models."
        ),
        expected_output=(
            "A structured summary with 3-5 bullet points, each containing "
            "a specific fact or insight from the reference material."
        ),
        agent=researcher,
    )

    write_task = Task(
        description=(
            "Using the research findings provided, write a 300-400 word report "
            "titled 'AI Agents in 2026: A State of the Field Overview'. "
            "Structure it with an introduction, 3 main sections (frameworks, "
            "production adoption, challenges), and a brief conclusion."
        ),
        expected_output=(
            "A complete report in markdown format with a title, introduction, "
            "3 sections with headings, and a conclusion. 300-400 words."
        ),
        agent=writer,
        context=[research_task],
    )

    edit_task = Task(
        description=(
            "Review and polish the report for: grammar and spelling, "
            "sentence flow and readability, conciseness (remove filler words), "
            "and overall structure. Return the final edited version."
        ),
        expected_output=(
            "The final polished report in markdown format, ready for "
            "publication. Same structure as the input but cleaner."
        ),
        agent=editor,
        context=[write_task],
    )

    print("All 3 tasks defined: research_task -> write_task (context) -> edit_task (context)")
    return research_task, write_task, edit_task


def run_research_crew():
    """Build and run the full research assistant crew, then save the report."""
    print("=" * 60)
    print("Research Assistant Crew (with tools)")
    print("=" * 60)

    reference_file = setup_reference_file()
    researcher, writer, editor = build_agents()
    research_task, write_task, edit_task = build_tasks(researcher, writer, editor, reference_file)

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_task, edit_task],
        process=Process.sequential,
        verbose=True,
    )
    print("Crew assembled. Agents:", [a.role for a in crew.agents], "Tasks:", len(crew.tasks))

    final_result = kickoff_with_retry(crew)
    print("\n" + "=" * 60)
    print("=== FINAL REPORT ===")
    print("=" * 60)
    print(final_result.raw)
    print("=" * 60)

    print("Output type :", type(final_result).__name__)
    print("Raw length  :", len(final_result.raw), "chars")
    print("Token usage :")
    print("  prompt_tokens    :", final_result.token_usage.prompt_tokens)
    print("  completion_tokens:", final_result.token_usage.completion_tokens)

    report_output = DATA_DIR / "final_report.md"
    report_output.write_text(final_result.raw, encoding="utf-8")
    print("\nReport saved to:", report_output)
    print("File size:", report_output.stat().st_size, "bytes")

    return final_result


if __name__ == "__main__":
    run_research_crew()
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    print("\nCleanup: removed", DATA_DIR)
