# Module 04: Human-in-the-Loop

> **MLCourse - Agentic AI - LangGraph**

Pausing graph execution for human input — using `interrupt()` and `Command(resume)` to build approval gates, review steps, and interactive breakpoints.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_interrupt_resume](01_interrupt_resume.ipynb) | Using `interrupt()` to pause execution and `Command(resume=...)` to continue |
| 02 | [02_approval_gates](02_approval_gates.ipynb) | Building human-approval checkpoints before sensitive tool calls or actions |
| 03 | [03_breakpoints_debugging](03_breakpoints_debugging.ipynb) | Using `interrupt_before` / `interrupt_after` breakpoints to inspect and debug state |

## Prerequisites

- Module 03 ([Persistence & Checkpointing](../03_persistence_checkpointing/README.md)) - `interrupt()` needs a checkpointer

## What you'll learn

- How `interrupt()` suspends execution and returns control to the human caller
- How `Command(resume=...)` feeds human input back into the graph
- How to design approval gates that require explicit human consent before proceeding
- How breakpoints let you step through and inspect graph execution interactively
