"""
01_installation_and_first_crew - Main Entry Point
=================================================

This is the main entry point that runs all parts of the module in sequence.
"""

import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import install_check
import cli_scaffolding
import first_crew


def main():
    """Run all parts of the Installation and First Crew module."""
    print("=" * 70)
    print("MODULE 01: INSTALLATION AND FIRST CREW")
    print("=" * 70)
    print()

    print("\n>>> Running Part 1: Install and Verify CrewAI")
    install_check.verify_crewai_installation()

    print("\n>>> Running Part 2: CLI Scaffolding")
    cli_scaffolding.run_cli_scaffolding()

    print("\n>>> Running Part 3: Your First Crew")
    first_crew.build_and_run_minimal_crew()
    first_crew.minimal_crew_template()

    print("\n" + "=" * 70)
    print("MODULE 01 COMPLETE")
    print("=" * 70)
    print("\nNext: Continue to 02_agents_deep_dive to understand agents in depth.")


if __name__ == "__main__":
    main()
