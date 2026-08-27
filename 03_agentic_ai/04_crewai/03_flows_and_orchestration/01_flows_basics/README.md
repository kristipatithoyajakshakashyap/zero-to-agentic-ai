# Module 01 - Flows Basics

> **MLCourse - Flows and Orchestration - Flows Basics**

CrewAI Flows provide a structured way to orchestrate multiple crews and tasks
using typed state, event-driven triggers, and listener functions. This module
introduces the Flow class, @start, @listen, and how to wire flows together.

## What you'll learn

- Define a Flow class with typed state
- Use @start to trigger the first step
- Use @listen to react to previous step outputs
- Define and pass typed state between steps
- Chain multiple steps in a flow

## Key concepts

- **Flow class**: the base class for defining orchestrated workflows
- **@start decorator**: marks the entry point of a flow
- **@listen decorator**: triggers a step when a previous step completes
- **Typed state**: Pydantic models that define the data flowing through a flow
- **Step chaining**: outputs of one step become inputs to the next

## Contents

1. `01_flow_basics.ipynb` - Flow class, @start, @listen, minimal flow
2. `02_typed_state.ipynb` - Pydantic state models, state passing between steps
3. `03_chaining_steps.ipynb` - multi-step flows, branching, convergence

After this module, continue to `02_flow_state_persistence` for checkpointing.
