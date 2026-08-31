"""
02_agents_deep_dive - Main Entry Point
=======================================

This is the main entry point that runs all parts of the module in sequence.
"""

import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import agent_parameters
import llm_assignment
import delegation
import max_iter
import verbose_reasoning
import config_approaches


def main():
    """Run all parts of the Agents Deep Dive module."""
    print("=" * 70)
    print("MODULE 02: AGENTS DEEP DIVE")
    print("=" * 70)
    print()

    print("\n>>> Running Part 1: Core Agent Parameters")
    agent_parameters.demonstrate_core_parameters()

    print("\n>>> Running Part 2: LLM Assignment")
    llm_assignment.demonstrate_llm_assignment()

    print("\n>>> Running Part 3: Delegation")
    delegation.demonstrate_delegation()

    print("\n>>> Running Part 4: max_iter")
    max_iter.demonstrate_max_iter()

    print("\n>>> Running Part 5: Verbose vs Reasoning")
    verbose_reasoning.demonstrate_verbose_reasoning()

    print("\n>>> Running Part 6: Configuration Approaches")
    config_approaches.demonstrate_config_approaches()

    print("\n" + "=" * 70)
    print("MODULE 02 COMPLETE")
    print("=" * 70)
    print("\nNext: Continue to 03_tasks_and_processes to learn about tasks and execution strategies.")


if __name__ == "__main__":
    main()
