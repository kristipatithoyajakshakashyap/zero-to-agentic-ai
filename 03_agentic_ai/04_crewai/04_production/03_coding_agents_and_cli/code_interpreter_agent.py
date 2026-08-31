"""code_interpreter_agent -- AGENTS.md format, sandboxed code execution
tool, code validation/retry pattern, and a real coding agent (Groq) that
writes and runs Python.

Uses a subprocess-based RunPython tool instead of CrewAI's optional
CodeInterpreterTool (which needs Docker) so this runs anywhere.

    python code_interpreter_agent.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _find_track() -> Path:
    p = Path(__file__).resolve()
    while p.name != "03_agentic_ai" and p.parent != p:
        p = p.parent
    return p


TRACK = _find_track()
load_dotenv(TRACK / ".env", override=False)


def get_llm(model: str = "qwen/qwen3.8-27b", temperature: float = 0.0, **kw) -> LLM:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            if requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            ).status_code == 200:
                return LLM(model=f"groq/{model}", api_key=api_key, temperature=temperature, **kw)
        except requests.RequestException:
            pass
    try:
        if requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200:
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=temperature, **kw)
    except requests.RequestException:
        pass
    raise RuntimeError("No LLM provider reachable. Set GROQ_API_KEY in 03_agentic_ai/.env or run local Ollama.")


AGENTS_MD_CONTENT = """# AGENTS.md -- Project Configuration for Coding Agents

## Project Overview
Demo project showing how coding agents interact with CrewAI.

## Directory Structure
- src/ : Application source code
- tests/ : Unit and integration tests
- data/ : Training and input data files

## Coding Conventions
- Python 3.11+ with type hints
- PEP 8 style
- All public functions must have docstrings

## Available Tools
- RunPython: Execute Python code in a sandboxed subprocess
- FileReadTool: Read file contents
- SerperDevTool: Web search (requires SERPER_API_KEY)

## Safety Rules
- Never execute code that modifies system files
- Always validate inputs before processing
- Use try/except for all external calls
"""


def write_agents_md() -> Path:
    data_dir = TRACK / "04_crewai" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "AGENTS.md"
    path.write_text(AGENTS_MD_CONTENT, encoding="utf-8")
    return path


@tool("RunPython")
def run_python(code: str) -> str:
    """Execute the given Python source code in a sandboxed subprocess and
    return its standard output (or error output)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Execution timed out after 30s"
    finally:
        os.unlink(tmp_path)


def validate_and_run(code: str, max_retries: int = 3) -> dict:
    """Execute code with validation and automatic retry on failure."""
    for attempt in range(max_retries):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp_path = f.name
        try:
            result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {"output": result.stdout, "success": True, "attempts": attempt + 1}
            print(f"  Attempt {attempt + 1} failed (return code {result.returncode})")
        finally:
            os.unlink(tmp_path)
    return {"output": "", "success": False, "attempts": max_retries}


def run_coding_agent_demo() -> str:
    llm = get_llm(temperature=0.7)
    coding_agent = Agent(
        role="Python Developer",
        goal="Write and execute Python code to solve computational problems.",
        backstory=(
            "You are an expert Python developer. You write clean, efficient code "
            "and verify your solutions by running them."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        tools=[run_python],
    )
    coding_task = Task(
        description=(
            "Write and run a Python script that calculates the first 10 Fibonacci "
            "numbers and their sum. Print the results clearly."
        ),
        expected_output="The first 10 Fibonacci numbers listed individually, followed by their sum.",
        agent=coding_agent,
    )
    coding_crew = Crew(agents=[coding_agent], tasks=[coding_task], process=Process.sequential, verbose=False)
    print("Running coding agent demo...")
    result = coding_crew.kickoff()
    print(f"\nAgent output:\n{str(result)[:500]}")
    return str(result)


if __name__ == "__main__":
    path = write_agents_md()
    print(f"AGENTS.md written to: {path}")

    print("\n=== RunPython tool direct call ===")
    print(run_python.run("print('fib =', sum([0,1,1,2,3,5,8,13,21,34]))"))

    print("=== Code validation and retry pattern ===")
    result = validate_and_run("print(sum(range(1, 101)))")
    print(f"  Success: {result['success']}, Attempts: {result['attempts']}, Output: {result['output'].strip()}")
    result = validate_and_run("print(undefined_variable)", max_retries=1)
    print(f"  Success: {result['success']}, Attempts: {result['attempts']}")

    print("\n=== Coding agent (Groq) demo ===")
    run_coding_agent_demo()
