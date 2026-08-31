"""main -- run the full coding_agents_and_cli module end to end.

    python main.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from cli_reference import CLI_COMMANDS, PROJECT_TREE, show_cli_help
from code_interpreter_agent import run_coding_agent_demo, validate_and_run, write_agents_md


def main() -> None:
    print("=== 1. AGENTS.md + sandboxed code execution ===")
    write_agents_md()
    validate_and_run("print(sum(range(1, 101)))")

    print("\n=== 2. CLI reference ===")
    show_cli_help(["--help"])
    print(PROJECT_TREE)

    print("\n=== 3. Coding agent demo (Groq) ===")
    run_coding_agent_demo()

    print("\n=== 4. CLI commands summary ===")
    for cmd, desc in CLI_COMMANDS:
        print(f"  {cmd:35s} {desc}")


if __name__ == "__main__":
    main()
