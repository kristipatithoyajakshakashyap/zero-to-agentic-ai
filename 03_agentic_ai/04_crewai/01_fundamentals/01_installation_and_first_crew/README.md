# Module 01 - Installation and First Crew

> **MLCourse - CrewAI Fundamentals - Installation and First Crew**

Get CrewAI running on your machine and build your first multi-agent crew from
scratch. This module covers installation, CLI scaffolding, and the minimal
Agent-Task-Crew triangle that every CrewAI application is built from.

## What you'll learn

- Install CrewAI and its optional tooling extras with pip
- Scaffold a new CrewAI project using the CLI
- Define agents with role, goal, and backstory
- Wire agents to tasks and run a crew end-to-end
- Understand the Agent-Task-Crew relationship

## Key concepts

- **Agent**: an autonomous unit with a role, goal, backstory, and optional LLM
- **Task**: a unit of work assigned to an agent with a description and expected output
- **Crew**: a team of agents executing a sequence of tasks
- **Process**: the execution strategy (sequential by default)
- **kickoff()**: the entry point that runs the crew

## Contents

1. `01_install_crewai.ipynb` - pip install walkthrough, version check, first crew
2. `02_cli_scaffolding.ipynb` - crewai create crew, project structure, run
3. `03_first_crew.ipynb` - minimal Agent-Task-Crew triangle, kickoff, output

After this module, continue to `02_agents_deep_dive` to understand agents in depth.
