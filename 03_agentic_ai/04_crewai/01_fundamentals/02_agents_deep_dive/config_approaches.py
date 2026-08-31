"""
02_agents_deep_dive - Part 6: Configuration Approaches
======================================================

Three ways to define agent configurations: Python constructor, JSON dict, JSON file.
"""

import sys
import json
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent_parameters import llm
from crewai import Agent


def demonstrate_config_approaches():
    """Show three approaches to agent configuration."""
    print("=" * 60)
    print("Agent Configuration Approaches")
    print("=" * 60)

    print("\n1. Python Constructor (Recommended)")
    print("-" * 40)
    python_agent = Agent(
        role="Code Reviewer",
        goal="Review Python code for bugs and style issues.",
        backstory=(
            "You are a senior Python developer with 15 years of experience. "
            "You catch subtle bugs and enforce PEP 8."
        ),
        llm=llm,
        tools=[],
        allow_delegation=False,
        max_iter=5,
        verbose=False,
        reasoning=False,
    )
    print("Created:", python_agent.role)
    print("Pros: IDE autocompletion, type safety, inline docs")
    print("Cons: Not externalizable to files")

    print("\n2. JSON Dictionary")
    print("-" * 40)
    agent_config = {
        "role": "Translator",
        "goal": "Translate English text to French accurately.",
        "backstory": (
            "You are a native French speaker with a background in "
            "technical translation."
        ),
        "llm": llm,
        "tools": [],
        "allow_delegation": False,
        "max_iter": 3,
        "verbose": False,
        "reasoning": False,
    }

    json_agent = Agent(**agent_config)
    print("Created:", json_agent.role)
    print("Goal:", json_agent.goal[:50])
    print("Pros: Dynamic, database-friendly")
    print("Cons: No type checking, LLM is special (must inject object)")

    print("\n3. JSON File")
    print("-" * 40)
    config_data = {
        "role": "Summarizer",
        "goal": "Condense long texts into 3 bullet points.",
        "backstory": "You are an expert at extracting key information.",
        "allow_delegation": False,
        "max_iter": 3,
        "verbose": False,
    }

    config_path = Path(tempfile.gettempdir()) / "agent_config.json"
    config_path.write_text(json.dumps(config_data, indent=2))
    print("Wrote config to:", config_path)

    loaded_config = json.loads(config_path.read_text())
    loaded_config["llm"] = llm
    loaded_config["tools"] = []

    file_agent = Agent(**loaded_config)
    print("Created:", file_agent.role)
    print("Goal:", file_agent.goal[:50])

    config_path.unlink(missing_ok=True)
    print("Pros: Version-control friendly, modular")
    print("Cons: File I/O overhead, same LLM note")

    print("\n" + "=" * 60)
    print("Comparison Table")
    print("=" * 60)
    print("| Approach           | Pros                              | Cons                          |")
    print("|--------------------|-----------------------------------|-------------------------------|")
    print("| Python constructor | IDE autocomplete, type safety     | Not externalizable            |")
    print("| JSON dict          | Dynamic, database-friendly        | No type checking, LLM special |")
    print("| JSON file          | Version-control friendly, modular | File I/O, same LLM note       |")

    print("\nAll three produce the same Agent object. Choose based on your project:")
    print("  - Prototyping: Python constructor")
    print("  - Config-driven systems: JSON/YAML file")
    print("  - Dynamic agent creation: JSON dict at runtime")


if __name__ == "__main__":
    demonstrate_config_approaches()
