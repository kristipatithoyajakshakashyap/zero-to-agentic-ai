"""app_spec -- the sample application specification the capstone pipeline
builds. This is plain data (a Python dict) -- no LLM calls here at all.

BEGINNER NOTE: in a real project, this spec would come from a product
manager or a client document. We hardcode it so every agent in the
pipeline sees exactly the same input every time you run this course.

    python app_spec.py
"""

from __future__ import annotations

import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

APP_SPEC = {
    "name": "TodoAPI",
    "description": "A simple REST API for managing todo items",
    "version": "1.0.0",
    "requirements": [
        "Create, read, update, and delete todo items",
        "Mark items as complete or incomplete",
        "Filter items by status (all, active, completed)",
        "Each item has: id, title, description, completed, created_at",
        "JSON request and response format",
        "Input validation and error handling",
    ],
    "tech_stack": {
        "backend": "FastAPI (Python)",
        "frontend": "React (TypeScript)",
        "database": "SQLite (via SQLAlchemy)",
        "testing": "pytest + React Testing Library",
    },
    "constraints": [
        "Must be self-contained (no external APIs)",
        "Code must include type hints",
        "All endpoints must have error handling",
        "Frontend must be responsive",
    ],
}


def spec_as_text() -> str:
    """Serialize the spec to a JSON string -- this is what gets passed into
    every Task's {spec} placeholder."""
    return json.dumps(APP_SPEC, indent=2)


if __name__ == "__main__":
    print("=== Application Specification ===")
    print(f"Name: {APP_SPEC['name']}")
    print(f"Description: {APP_SPEC['description']}")
    print(f"Requirements: {len(APP_SPEC['requirements'])} items")
    print(f"Tech stack: {list(APP_SPEC['tech_stack'].keys())}")
    print(f"Constraints: {len(APP_SPEC['constraints'])} items")
