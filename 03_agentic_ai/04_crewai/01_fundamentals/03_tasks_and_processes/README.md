# Module 03 - Tasks and Processes

> **MLCourse - CrewAI Fundamentals - Tasks and Processes**

Tasks are the units of work agents execute. This module covers task description,
expected output, agent assignment, context passing between tasks, and the two
process strategies: sequential (linear handoff) and hierarchical (manager agent
delegates).

## What you'll learn

- Define tasks with description, expected output, and agent assignment
- Pass context between sequential tasks
- Choose between sequential and hierarchical processes
- Kick off crews asynchronously
- Use the manager agent pattern effectively

## Key concepts

- **Task**: work unit with description, expected_output, and agent
- **context**: prior task outputs available to the current task
- **sequential process**: tasks run in order, each receiving prior outputs
- **hierarchical process**: a manager agent delegates to worker agents
- **async kickoff**: kick_off_async() for non-blocking execution

## Contents

1. `01_task_basics.ipynb` - description, expected_output, agent, context
2. `02_sequential_vs_hierarchical.ipynb` - process types, when to use each
3. `03_async_kickoff.ipynb` - kick_off_async, gather, parallel execution

After this module, continue to `04_built_in_tools` to learn about CrewAI's tool catalog.
