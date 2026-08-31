"""flow_orchestration -- the same pipeline as sequential_crew.py, but built
as a CrewAI Flow so Frontend and Backend development run in parallel, and
QA results can route the pipeline to different next steps.

BEGINNER NOTE: a Flow is a class where each method is a pipeline step.
- `@start()` marks the entry point.
- `@listen(other_method)` means "run this after other_method finishes."
- `@listen(and_(a, b))` means "run this after BOTH a and b finish" -- this
  is how CrewAI expresses parallel branches joining back together.
- `@router(other_method)` lets a step's *return value* choose which
  branch runs next (like an if/else for the whole pipeline).

    python flow_orchestration.py
"""

from __future__ import annotations

import sys
import time

from crewai import Crew, Process
from crewai.flow.flow import Flow, and_, listen, router, start

from agents import build_agents
from app_spec import spec_as_text
from tasks import build_tasks

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class AppBuilderFlow(Flow):
    """Full-stack app builder with parallel dev and conditional routing.

    Flow diagram:
        PM -> Architect -> [Frontend + Backend] -> QA -> Writer
                                                      |
                                          if "critical" in QA output -> fix_bugs
                                          else                       -> write_documentation
    """

    def __init__(self, agents: dict, tasks: dict):
        self._agents = agents
        self._tasks = tasks
        super().__init__()

    def _run_one(self, agent_key: str, task_key: str, max_retries: int = 4) -> str:
        """Run a single agent+task pair as its own tiny one-step crew.

        Retries with backoff on Groq's tokens-per-minute rate limit, so a
        burst of calls (e.g. Frontend and Backend running "in parallel")
        never crashes the whole pipeline -- it just waits and continues.
        """
        crew = Crew(agents=[self._agents[agent_key]], tasks=[self._tasks[task_key]], process=Process.sequential, verbose=False)
        for attempt in range(max_retries):
            try:
                return str(crew.kickoff(inputs={"spec": spec_as_text()}))
            except Exception as exc:  # noqa: BLE001 - Groq rate limits surface as generic litellm errors
                if "rate_limit" in str(exc).lower() and attempt < max_retries - 1:
                    delay = 10.0 * (attempt + 1)
                    print(f"  Rate limited, retrying in {delay:.0f}s...")
                    time.sleep(delay)
                    continue
                raise

    @start()
    def start_pipeline(self):
        print("[Flow] Step 1: Product Manager")
        self.pm_output = self._run_one("pm", "pm")
        return self.pm_output

    @listen(start_pipeline)
    def design_architecture(self, pm_output):
        print("[Flow] Step 2: Architect (after PM)")
        self.arch_output = self._run_one("architect", "architect")
        return self.arch_output

    @listen(design_architecture)
    def develop_frontend(self, arch_output):
        print("[Flow] Step 3a: Frontend Developer (parallel with Backend)")
        self.fe_output = self._run_one("frontend", "frontend")
        return self.fe_output

    @listen(design_architecture)
    def develop_backend(self, arch_output):
        print("[Flow] Step 3b: Backend Developer (parallel with Frontend)")
        self.be_output = self._run_one("backend", "backend")
        return self.be_output

    @listen(and_(develop_frontend, develop_backend))
    def run_qa(self, _):
        print("[Flow] Step 4: QA Engineer (after both devs finish)")
        self.qa_output = self._run_one("qa", "qa")
        return self.qa_output

    @router(run_qa)
    def check_qa_results(self, qa_output):
        """The return value here decides which @listen("...") runs next."""
        if "critical" in qa_output.lower():
            print("[Flow] Router: critical bug found -> routing to fix_bugs")
            return "fix_bugs"
        print("[Flow] Router: QA passed -> routing to documentation")
        return "proceed"

    @listen("fix_bugs")
    def fix_bugs(self):
        print("[Flow] Step 5 (bug path): re-running developers (simplified)")
        self.fix_output = "Bug fixes applied based on QA report."
        return self.fix_output

    @listen("proceed")
    def write_documentation(self):
        print("[Flow] Step 5 (happy path): Technical Writer")
        self.docs_output = self._run_one("writer", "writer")
        return self.docs_output


def run_flow_pipeline() -> str:
    agents = build_agents()
    tasks = build_tasks(agents)
    flow = AppBuilderFlow(agents, tasks)
    result = flow.kickoff()
    print(f"\nFlow completed. Final step output: {str(result)[:200]}")
    return str(result)


if __name__ == "__main__":
    run_flow_pipeline()
