"""
04_built_in_tools - Part 5: Agents with Multiple Tools
=========================================================

Covers: assigning tools to agents, running tools standalone, defensive
error-handling patterns for tool output, and the full agent+tools+task+crew
pattern with a real Groq-backed agent that reads and writes files.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from llm_setup import llm, kickoff_with_retry
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool

DEMO_DIR = Path.cwd() / "_crewai_tools_demo"


def setup_demo_dir() -> Path:
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    DEMO_DIR.mkdir(parents=True)
    sample_file = DEMO_DIR / "sample_data.txt"
    sample_file.write_text(
        "Name,Score,Grade\n"
        "Alice,95,A\n"
        "Bob,82,B\n"
        "Charlie,91,A\n"
        "Diana,76,C\n"
    )
    return sample_file


def demonstrate_agent_with_tools(sample_file: Path):
    """Assign FileReadTool + DirectoryReadTool to an agent and run it.

    The key idea: an Agent's `tools=[...]` list is just Python objects with
    a `.run()` method. The LLM reads each tool's name/description and
    decides for itself, mid-task, when and how to call one - you never
    call the tool manually once it's wired into an agent like this.
    """
    print("=" * 60)
    print("Assigning Tools to an Agent")
    print("=" * 60)

    file_agent = Agent(
        role="File Analyst",
        goal="Read and summarize file contents from the data directory.",
        backstory=(
            "You are a meticulous analyst who reads files carefully "
            "and produces accurate summaries."
        ),
        llm=llm,
        tools=[
            FileReadTool(),
            DirectoryReadTool(),
        ],
        allow_delegation=False,
        verbose=True,
    )

    file_task = Task(
        description=(
            "Read all files in the data directory and provide a summary "
            f"of each file's contents. Directory: {DEMO_DIR}"
        ),
        expected_output="A summary of each file found in the directory.",
        agent=file_agent,
    )

    file_crew = Crew(agents=[file_agent], tasks=[file_task], process=Process.sequential, verbose=False)
    file_result = kickoff_with_retry(file_crew)
    print("\n=== File Analysis ===")
    print(file_result.raw)


def demonstrate_standalone_tool_usage(sample_file: Path):
    """Every CrewAI tool has a .run() method usable outside of an agent."""
    print("\n" + "=" * 60)
    print("Standalone Tool Usage")
    print("=" * 60)

    reader = FileReadTool()
    raw = reader.run(file_path=str(sample_file))
    print("Return type:", type(raw).__name__)
    print("Content preview:", str(raw)[:200])
    print("Line count:", str(raw).count("\n"))

    writer = FileWriterTool()
    writer.run(filename="standalone_output.txt", directory=str(DEMO_DIR), content="Written by standalone FileWriterTool.run()", overwrite=True)
    standalone_output = DEMO_DIR / "standalone_output.txt"
    print("\nStandalone write complete:", standalone_output.read_text())


def demonstrate_error_handling(sample_file: Path):
    """Defensive patterns for tool output - modern crewai_tools return error
    strings instead of raising on most failures."""
    print("\n" + "=" * 60)
    print("Tool Error Handling Patterns")
    print("=" * 60)

    # Pattern 1: check the returned string for an error marker.
    reader = FileReadTool()
    nonexistent = DEMO_DIR / "does_not_exist.txt"
    content = reader.run(file_path=str(nonexistent))
    if content.startswith("Error:"):
        print("[expected error] File not found ->", content)
    else:
        print("Content:", content)

    # Pattern 2: pre-check before calling tool.run().
    writer = FileWriterTool()
    safe_path = DEMO_DIR / "safe_output.txt"
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    safe_result = writer.run(filename="safe_output.txt", directory=str(DEMO_DIR), content="Safe write succeeded.", overwrite=True)
    print("Safe write:", safe_result)

    # Pattern 3: validate tool output before using it.
    reader = FileReadTool()
    raw_output = reader.run(file_path=str(sample_file))
    if raw_output and "Alice" in str(raw_output):
        print("\nValidation passed: file contains expected data.")
    else:
        print("\nValidation warning: unexpected file content.")


def demonstrate_full_pattern(sample_file: Path):
    """Complete pattern: agent with read+write tools, task, crew."""
    print("\n" + "=" * 60)
    print("Complete Pattern: Agent + Tools + Task + Crew")
    print("=" * 60)

    analyst_agent = Agent(
        role="Data Analyst",
        goal="Read data, analyze it, and save a report.",
        backstory="You are a thorough data analyst.",
        llm=llm,
        tools=[
            FileReadTool(),
            FileWriterTool(),
        ],
        allow_delegation=False,
        verbose=True,
    )

    report_path = DEMO_DIR / "analysis_report.txt"
    analysis_task = Task(
        description=(
            f"Read the CSV file at {sample_file}, calculate the average "
            f"score, and write a summary report to {report_path} "
            "using the FileWriterTool (pass overwrite=True)."
        ),
        expected_output="A report file written to disk with the average score and a brief analysis.",
        agent=analyst_agent,
    )

    analysis_crew = Crew(agents=[analyst_agent], tasks=[analysis_task], process=Process.sequential, verbose=False)
    analysis_result = kickoff_with_retry(analysis_crew)
    print("\n=== Analysis Result ===")
    print(analysis_result.raw)

    if report_path.exists():
        print("\n=== Report on Disk ===")
        print(report_path.read_text())


if __name__ == "__main__":
    sample = setup_demo_dir()
    demonstrate_agent_with_tools(sample)
    demonstrate_standalone_tool_usage(sample)
    demonstrate_error_handling(sample)
    demonstrate_full_pattern(sample)
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    print("\nCleanup: removed", DEMO_DIR)
