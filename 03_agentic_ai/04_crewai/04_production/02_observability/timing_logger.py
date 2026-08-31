"""timing_logger -- a custom BaseEventListener subclass that tracks agent
and task execution durations, runs it against a real Groq crew, and
exports the captured timeline to data/crew_trace.json.

    python timing_logger.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.events.base_event_listener import BaseEventListener
from crewai.events.types.agent_events import (
    AgentExecutionCompletedEvent,
    AgentExecutionStartedEvent,
)
from crewai.events.types.crew_events import (
    CrewKickoffCompletedEvent,
    CrewKickoffStartedEvent,
)
from crewai.events.types.task_events import TaskCompletedEvent, TaskStartedEvent
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


class TimingLogger(BaseEventListener):
    """Custom event listener tracking wall-clock duration per agent/task."""

    def setup_listeners(self, crewai_event_bus):
        crewai_event_bus.on(CrewKickoffStartedEvent)(self.crew_start)
        crewai_event_bus.on(CrewKickoffCompletedEvent)(self.crew_end)
        crewai_event_bus.on(AgentExecutionStartedEvent)(self.agent_start)
        crewai_event_bus.on(AgentExecutionCompletedEvent)(self.agent_end)
        crewai_event_bus.on(TaskStartedEvent)(self.task_start)
        crewai_event_bus.on(TaskCompletedEvent)(self.task_end)

    def __init__(self):
        self.timeline: list[dict] = []
        self.agent_starts: dict[str, float] = {}
        self.agent_durations: dict[str, list[float]] = {}
        self.crew_start_time: float | None = None
        self.crew_end_time: float | None = None
        super().__init__()

    def _record(self, event_type: str, **kwargs) -> None:
        self.timeline.append({"event": event_type, "timestamp": time.time(), **kwargs})

    def _role(self, event) -> str:
        agent = getattr(event, "agent", None)
        return agent.get("role", "unknown") if isinstance(agent, dict) else getattr(agent, "role", "unknown")

    def crew_start(self, source, event):
        self.crew_start_time = time.time()
        self._record("crew_start")
        print(f"  [TimingLogger] Crew started at {self.crew_start_time:.3f}")

    def crew_end(self, source, event):
        self.crew_end_time = time.time()
        duration = self.crew_end_time - (self.crew_start_time or self.crew_end_time)
        self._record("crew_end", duration_s=round(duration, 3))
        print(f"  [TimingLogger] Crew ended -- total {duration:.3f}s")

    def agent_start(self, source, event):
        role = self._role(event)
        self.agent_starts[role] = time.time()
        self._record("agent_start", agent=role)
        print(f"  [TimingLogger] Agent '{role}' started")

    def agent_end(self, source, event):
        role = self._role(event)
        start = self.agent_starts.pop(role, time.time())
        duration = time.time() - start
        self.agent_durations.setdefault(role, []).append(duration)
        self._record("agent_end", agent=role, duration_s=round(duration, 3))
        print(f"  [TimingLogger] Agent '{role}' ended -- {duration:.3f}s")

    def task_start(self, source, event):
        self._record("task_start")

    def task_end(self, source, event):
        self._record("task_end")

    def summary(self) -> None:
        print("\n=== TimingLogger Summary ===")
        if self.crew_start_time and self.crew_end_time:
            print(f"Total crew time: {self.crew_end_time - self.crew_start_time:.3f}s")
        print(f"Events recorded: {len(self.timeline)}")
        for role, durations in self.agent_durations.items():
            print(f"  {role}: avg={sum(durations) / len(durations):.3f}s ({len(durations)} runs)")

    def to_json(self) -> str:
        return json.dumps(self.timeline, indent=2, default=str)


def run_timed_crew() -> TimingLogger:
    llm = get_llm(temperature=0.7)
    timed_agent = Agent(
        role="Analyst",
        goal="Analyze the given data point and provide insights.",
        backstory="You are a data analyst who provides clear, concise insights.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )
    timed_task = Task(
        description="Analyze the trend: AI adoption increased 40% in 2025. Respond with a short analysis.",
        expected_output="A 2-3 sentence analysis of the AI adoption trend.",
        agent=timed_agent,
    )
    timed_crew = Crew(agents=[timed_agent], tasks=[timed_task], process=Process.sequential, verbose=False)

    logger = TimingLogger()
    print("Running crew with TimingLogger attached...")
    result = timed_crew.kickoff()
    time.sleep(0.5)
    logger.summary()
    print(f"\nCrew output: {str(result)[:100]}")
    return logger


def export_trace(logger: TimingLogger) -> Path:
    data_dir = TRACK / "04_crewai" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    trace_file = data_dir / "crew_trace.json"
    trace_file.write_text(logger.to_json(), encoding="utf-8")
    return trace_file


if __name__ == "__main__":
    logger = run_timed_crew()
    trace_file = export_trace(logger)
    print(f"\nTrace data exported to: {trace_file}")
    print(f"Events exported: {len(logger.timeline)}")
