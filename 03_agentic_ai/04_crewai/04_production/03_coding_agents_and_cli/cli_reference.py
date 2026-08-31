"""cli_reference -- crewai CLI commands (create crew, run, test, train, flow),
scaffolded project structure, and live `crewai --help` / `crewai run --help`
output from the CLI actually installed in this environment.

    python cli_reference.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_TREE = """
my_project/
|-- src/my_project/
|   |-- __init__.py
|   |-- main.py          # Crew class with @agent, @task decorators
|   |-- agents.py        # Agent definitions (role, goal, backstory)
|   |-- tasks.py         # Task definitions (description, expected_output)
|   |-- tools.py         # Custom tool implementations
|-- tests/
|   |-- test_main.py     # Crew behavior tests
|-- pyproject.toml       # Dependencies and project metadata
|-- .env.example         # Environment variable template
|-- AGENTS.md            # Coding agent instructions
|-- README.md            # Human-readable documentation
"""

SAMPLE_MAIN_PY = '''
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class MyProject:
    """Main crew definition for MyProject."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)
'''

CLI_COMMANDS = [
    ("crewai create crew NAME", "Scaffold a new crew project with standard structure"),
    ("crewai run", "Execute the crew defined in src/main.py"),
    ("crewai run --inputs '{...}'", "Execute with custom JSON inputs"),
    ("crewai test", "Run crew once for quick validation"),
    ("crewai test --crew NAME", "Test a specific crew by name"),
    ("crewai train --n NUM", "Train crew prompts over NUM iterations"),
    ("crewai flow", "Execute a Flow defined in the project"),
]


def _find_crewai_cli() -> str:
    return shutil.which("crewai") or os.path.join(os.path.dirname(sys.executable), "crewai.exe")


def show_cli_help(args: list[str]) -> None:
    cli = _find_crewai_cli()
    result = subprocess.run([cli, *args], capture_output=True, text=True, timeout=30)
    print(f"=== crewai {' '.join(args)} ===")
    print((result.stdout or result.stderr or "No output")[:1500])


if __name__ == "__main__":
    show_cli_help(["--help"])

    print("\n=== Scaffolded project structure (crewai create crew) ===")
    print(PROJECT_TREE)
    print("=== Sample main.py ===")
    print(SAMPLE_MAIN_PY)

    print()
    show_cli_help(["run", "--help"])

    print("\n=== CrewAI CLI Commands Reference ===")
    for cmd, desc in CLI_COMMANDS:
        print(f"  {cmd:35s} {desc}")
