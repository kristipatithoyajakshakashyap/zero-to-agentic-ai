"""metrics -- simple quality metrics you can compute on any agent's text
output, plus the production deployment checklist for this capstone.

BEGINNER NOTE: these are intentionally simple heuristics (word counts,
"does it contain a code block") -- not LLM calls. In a real system you'd
combine cheap heuristics like these with periodic human review before
trusting generated code.

    python metrics.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def analyze_output(text: str, label: str) -> dict:
    """Compute basic quality metrics for a chunk of agent output text."""
    lines = text.strip().split("\n")
    words = text.split()
    return {
        "label": label,
        "lines": len(lines),
        "words": len(words),
        "code_blocks": text.count("```") // 2,
        "headers": sum(1 for line in lines if line.startswith("#")),
        "bullet_points": sum(1 for line in lines if line.strip().startswith(("-", "*"))),
        "has_types": "def " in text and ":" in text,
        "has_docstrings": '"""' in text or "'''" in text,
    }


QUALITY_CHECKLIST = [
    ("Type hints present", "Has def and : annotations"),
    ("Docstrings present", "Has triple-quote strings"),
    ("Error handling", "Has try/except blocks"),
    ("Input validation", "Has Pydantic models"),
    ("Tests included", "Has assert or test_ functions"),
    ("README included", "Has # headers and setup instructions"),
]

DEPLOYMENT_CHECKLIST = [
    "Human code review completed",
    "Backend tests pass (pytest)",
    "Frontend tests pass (npm test)",
    "No hardcoded secrets",
    "Error handling covers edge cases",
    "Documentation complete",
    "Database migrations reversible",
    "Logging configured",
    "Rate limiting enabled",
    "Security review completed",
]


if __name__ == "__main__":
    sample_output = """# User Stories

## Story 1: Create Todo
- As a user, I want to create a new todo item
- Acceptance criteria:
  - POST /todos accepts title and description
  - Returns 201 with created item
"""
    metrics = analyze_output(sample_output, "User Stories")
    print("Sample output metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    print("\nQuality checklist for generated code:")
    for item, check in QUALITY_CHECKLIST:
        print(f"  [ ] {item:25s} -- {check}")

    print("\n=== Production Deployment Checklist ===")
    for idx, item in enumerate(DEPLOYMENT_CHECKLIST, 1):
        print(f"  {idx:2d}. [ ] {item}")
