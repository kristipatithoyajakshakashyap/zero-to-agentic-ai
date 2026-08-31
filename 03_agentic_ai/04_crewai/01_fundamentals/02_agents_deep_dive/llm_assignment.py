"""
02_agents_deep_dive - Part 2: LLM Assignment
=============================================

CrewAI lets you assign a different LLM to each agent. This is powerful:
use a fast, small model for simple tasks and a larger model for complex reasoning.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent_parameters import get_llm
from crewai import Agent


def demonstrate_llm_assignment():
    """Show how to assign different LLMs to different agents."""
    print("=" * 60)
    print("LLM Assignment - Different Models Per Agent")
    print("=" * 60)

    llm_fast = get_llm(model="qwen/qwen3.6-27b")

    agent_fast = Agent(
        role="Quick Summarizer",
        goal="Produce a one-sentence summary.",
        backstory="You are fast and concise.",
        llm=llm_fast,
        allow_delegation=False,
        verbose=False,
    )

    llm_deep = get_llm(model="qwen/qwen3.8-27b")

    agent_deep = Agent(
        role="Deep Analyst",
        goal="Provide a thorough multi-paragraph analysis.",
        backstory="You are thorough and methodical.",
        llm=llm_deep,
        allow_delegation=False,
        max_iter=10,
        verbose=False,
    )

    print("Fast agent LLM:", agent_fast.llm.model)
    print("Deep agent LLM :", agent_deep.llm.model)
    print("Same model?    :", agent_fast.llm.model == agent_deep.llm.model)

    print("\nUse cases:")
    print("  - Smaller Groq model: Simple extraction, classification, summarization")
    print("  - Larger Groq model : Complex reasoning, planning, coding")
    print("  - Groq: When you need reliability and speed for tool calling")


if __name__ == "__main__":
    demonstrate_llm_assignment()
