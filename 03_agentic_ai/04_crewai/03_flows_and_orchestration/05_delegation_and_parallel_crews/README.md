# Module 05 - Delegation and Parallel Crews

> **MLCourse - Flows and Orchestration - Delegation and Parallel Crews**

Complex workflows often require multiple crews working together. This module
covers delegation chains (one crew handing off to another) and parallel crew
execution for independent tasks that can run simultaneously.

## What you'll learn

- Design delegation chains where one crew's output feeds another
- Execute independent crews in parallel for speed
- Manage shared state between parallel crews
- Aggregate results from multiple crew runs
- Choose between sequential delegation and parallel execution

## Key concepts

- **Delegation chain**: sequential crew execution where output feeds input
- **Parallel crews**: independent crews running simultaneously
- **Shared state**: passing data between crews in a flow
- **Result aggregation**: combining outputs from parallel runs
- **Crew composition**: deciding when to split work across crews

## Contents

1. `01_delegation_chains.ipynb` - sequential crew handoff, output chaining
2. `02_parallel_crews.ipynb` - concurrent execution, asyncio, gather
3. `03_aggregation.ipynb` - combining parallel results, conflict resolution

After this module, continue to `04_production` for testing and deployment.
