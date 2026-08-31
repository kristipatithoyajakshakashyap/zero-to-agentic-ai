"""
01_installation_and_first_crew - Part 2: CLI Scaffolding
========================================================

This module covers using the CrewAI CLI to scaffold a new project.
"""


def run_cli_scaffolding() -> None:
    """Demonstrate CrewAI CLI scaffolding."""
    print("CrewAI CLI Commands:")
    print("  crewai create crew <project_name>  - Create a new crew project")
    print("  crewai create agent <agent_name>   - Add an agent to existing project")
    print("  crewai create task <task_name>     - Add a task to existing project")
    print("  crewai run                         - Run the crew")
    print("  crewai test                        - Run tests")

    print("\nProject structure created by 'crewai create crew my_crew':")
    print("  my_crew/")
    print("  |-- pyproject.toml")
    print("  |-- src/")
    print("  |   |-- my_crew/")
    print("  |       |-- __init__.py")
    print("  |       |-- main.py")
    print("  |       |-- crew.py")
    print("  |       |-- agents.yaml")
    print("  |       |-- tasks.yaml")
    print("  |-- tests/")
    print("      |-- test_crew.py")

    print("\n[NOTE] Run 'crewai create crew my_project' in your terminal to scaffold a project.")


if __name__ == "__main__":
    print("=" * 60)
    print("Part 2: CLI Scaffolding")
    print("=" * 60)
    run_cli_scaffolding()
