"""
03_tasks_and_processes - Main Entry Point
==========================================

This is the main entry point that runs all parts of the module in sequence.
"""

import sys
import time
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import task_basics
import sequential_hierarchical
import context_passing
import callbacks
import output_parsing
import async_kickoff
import batch_kickoff_for_each


def main():
    """Run all parts of the Tasks and Processes module."""
    print("=" * 70)
    print("MODULE 03: TASKS AND PROCESSES")
    print("=" * 70)
    print()

    # Small pauses between parts keep this module under Groq's free-tier
    # tokens-per-minute cap when running the whole sequence back to back.
    pause = 12

    print("\n>>> Running Part 1: Task Basics")
    task_basics.demonstrate_task_parameters()
    time.sleep(pause)

    print("\n>>> Running Part 2: Sequential vs Hierarchical")
    sequential_hierarchical.demonstrate_sequential()
    time.sleep(pause)
    sequential_hierarchical.demonstrate_hierarchical()
    time.sleep(pause)

    print("\n>>> Running Part 3: Context Passing")
    context_passing.demonstrate_context_passing()
    time.sleep(pause)

    print("\n>>> Running Part 4: Callbacks")
    callbacks.demonstrate_callbacks()
    time.sleep(pause)

    print("\n>>> Running Part 5: Output Parsing")
    output_parsing.demonstrate_output_parsing()
    time.sleep(pause)

    print("\n>>> Running Part 6: Async Kickoff")
    async_kickoff.demonstrate_async_kickoff()
    time.sleep(pause)

    print("\n>>> Running Part 7: Batch Execution (kickoff_for_each)")
    batch_kickoff_for_each.demonstrate_batch_kickoff_for_each()

    print("\n" + "=" * 70)
    print("MODULE 03 COMPLETE")
    print("=" * 70)
    print("\nNext: Continue to 04_built_in_tools to learn about CrewAI's built-in tools.")


if __name__ == "__main__":
    main()
