"""tasks -- the six tasks the capstone pipeline runs, one per agent.

BEGINNER NOTE: a Task's `description` is the actual prompt the agent sees;
`expected_output` tells the agent (and you, reading the code) what a good
answer looks like; `context=[other_task]` lets one task's output flow into
the next task's prompt automatically -- that's how CrewAI chains agents.

Descriptions here are kept short (compared to a "real" spec) on purpose:
Groq's free tier has a tight tokens-per-minute limit, and a course should
run reliably without hitting it.

    python tasks.py
"""

from __future__ import annotations

import sys

from crewai import Agent, Task

from agents import build_agents

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_tasks(agents: dict[str, Agent]) -> dict[str, Task]:
    pm_task = Task(
        description=(
            "Read this spec: {spec}\n"
            "List 3 user stories (title + 'As a X, I want Y, so that Z' + one acceptance criterion each). Be brief."
        ),
        expected_output="3 short user stories with acceptance criteria.",
        agent=agents["pm"],
    )

    architect_task = Task(
        description=(
            "Based on the user stories, briefly design: 1) the DB table (columns+types), "
            "2) the 4 CRUD API endpoints (method+path). Keep it to a short list, no prose."
        ),
        expected_output="A short DB schema and a list of API endpoints.",
        agent=agents["architect"],
        context=[pm_task],
    )

    frontend_task = Task(
        description="Name the 3 React components needed for this UI and one line on what each does. Be brief.",
        expected_output="A short list of component names with one-line descriptions.",
        agent=agents["frontend"],
        context=[architect_task],
    )

    backend_task = Task(
        description="Name the FastAPI route functions needed to implement the endpoints. One line each. Be brief.",
        expected_output="A short list of route function names with one-line descriptions.",
        agent=agents["backend"],
        context=[architect_task],
    )

    qa_task = Task(
        description="List 3 test cases (happy path, edge case, error case) for this API. One line each. Be brief.",
        expected_output="3 short test case descriptions.",
        agent=agents["qa"],
        context=[frontend_task, backend_task],
    )

    writer_task = Task(
        description="Write a 3-sentence README summary for this project covering purpose, stack, and how to run it.",
        expected_output="A short README summary paragraph.",
        agent=agents["writer"],
        context=[pm_task, architect_task, frontend_task, backend_task],
    )

    return {
        "pm": pm_task,
        "architect": architect_task,
        "frontend": frontend_task,
        "backend": backend_task,
        "qa": qa_task,
        "writer": writer_task,
    }


if __name__ == "__main__":
    agents = build_agents()
    tasks = build_tasks(agents)
    print(f"All {len(tasks)} tasks defined:")
    for key, task in tasks.items():
        print(f"  {key:10s} ({task.agent.role}): {task.description[:60]}...")
