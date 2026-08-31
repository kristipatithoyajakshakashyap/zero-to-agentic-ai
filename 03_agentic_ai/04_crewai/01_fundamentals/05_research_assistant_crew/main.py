"""
05_research_assistant_crew - Main Entry Point
================================================

Runs the full research crew (with tools) and the tool-free variant.
"""

import sys
import time
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import llm_setup  # noqa: F401
import research_crew
import basic_variant_no_tools


def main():
    print("=" * 70)
    print("MODULE 05: RESEARCH ASSISTANT CREW (FUNDAMENTALS CAPSTONE)")
    print("=" * 70)

    print("\n>>> Part 1: Full Research Crew (with tools)")
    research_crew.run_research_crew()
    research_crew.shutil.rmtree(research_crew.DATA_DIR, ignore_errors=True)

    time.sleep(65)

    print("\n>>> Part 2: Basic Variant (no tools)")
    basic_variant_no_tools.run_basic_crew()

    print("\n" + "=" * 70)
    print("MODULE 05 COMPLETE - FUNDAMENTALS PHASE FINISHED")
    print("=" * 70)
    print("\nNext: Continue to 02_advanced_agents to learn custom tools, knowledge sources, and memory.")


if __name__ == "__main__":
    main()
