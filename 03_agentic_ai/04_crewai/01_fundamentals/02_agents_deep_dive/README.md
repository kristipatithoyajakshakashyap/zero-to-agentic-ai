# Module 02 - Agents Deep Dive

> **MLCourse - CrewAI Fundamentals - Agents Deep Dive**

Every CrewAI agent is defined by three things: a role, a goal, and a backstory.
This module unpacks each parameter, shows how to assign different LLMs to different
agents, and introduces delegation - the mechanism that lets agents hand off work to
each other.

## What you'll learn

- Define agent role, goal, and backstory effectively
- Assign different LLMs to different agents within the same crew
- Enable and control agent delegation
- Use allow_delegation and max_iter parameters
- Write backstories that shape agent behavior

## Key concepts

- **role**: the job title or function the agent performs
- **goal**: the objective the agent strives toward
- **backstory**: narrative context that guides decision-making style
- **LLM assignment**: override the default model per agent
- **delegation**: agents requesting help from other agents in the crew

## Contents

1. `01_agent_parameters.ipynb` - role/goal/backstory deep dive, examples
2. `02_llm_assignment.ipynb` - different models per agent, Ollama/Groq/OpenAI
3. `03_delegation.ipynb` - allow_delegation, when agents ask for help

After this module, continue to `03_tasks_and_processes` to learn about tasks and execution strategies.
