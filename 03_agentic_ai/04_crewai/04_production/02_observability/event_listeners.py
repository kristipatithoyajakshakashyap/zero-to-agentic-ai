"""event_listeners -- CrewAI's event bus, event types, and a minimal
@crewai_event_bus.on() subscription demo, run against a real Groq crew.

    python event_listeners.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import requests
from crewai import LLM, Agent, Crew, Process, Task
from crewai.events.event_bus import crewai_event_bus
from crewai.events.types.agent_events import (
    AgentExecutionCompletedEvent,
    AgentExecutionStartedEvent,
)
from crewai.events.types.crew_events import (
    CrewKickoffCompletedEvent,
    CrewKickoffStartedEvent,
)
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _find_track() -> Path:
    p = Path(__file__).resolve()
    while p.name != "03_agentic_ai" and p.parent != p:
        p = p.parent
    return p


load_dotenv(_find_track() / ".env", override=False)


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


EVENT_TYPES_REFERENCE = [
    ("CrewKickoffStartedEvent", "Crew begins execution"),
    ("CrewKickoffCompletedEvent", "Crew finishes execution"),
    ("AgentExecutionStartedEvent", "Agent begins a task"),
    ("AgentExecutionCompletedEvent", "Agent finishes a task"),
]


def run_event_bus_demo() -> list[dict]:
    """Register handlers on the global event bus and run a real crew."""
    llm = get_llm()
    monitor_agent = Agent(
        role="Monitor",
        goal="Perform a simple verification task.",
        backstory="You are a monitoring agent that checks system status.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )
    monitor_task = Task(
        description="Verify the monitoring system is operational. Respond with the single word: operational.",
        expected_output="A status report indicating the system is operational.",
        agent=monitor_agent,
    )
    monitor_crew = Crew(agents=[monitor_agent], tasks=[monitor_task], process=Process.sequential, verbose=False)

    events_log: list[dict] = []

    @crewai_event_bus.on(CrewKickoffStartedEvent)
    def on_crew_start(source, event):
        events_log.append({"type": "crew_start", "time": time.time()})
        print("[EVENT] Crew started")

    @crewai_event_bus.on(CrewKickoffCompletedEvent)
    def on_crew_end(source, event):
        events_log.append({"type": "crew_end", "time": time.time()})
        print("[EVENT] Crew ended")

    @crewai_event_bus.on(AgentExecutionStartedEvent)
    def on_agent_start(source, event):
        role = getattr(event.agent, "role", "unknown") if not isinstance(event.agent, dict) else event.agent.get("role", "unknown")
        events_log.append({"type": "agent_start", "time": time.time(), "role": role})
        print(f"[EVENT] Agent started: {role}")

    @crewai_event_bus.on(AgentExecutionCompletedEvent)
    def on_agent_end(source, event):
        role = getattr(event.agent, "role", "unknown") if not isinstance(event.agent, dict) else event.agent.get("role", "unknown")
        events_log.append({"type": "agent_end", "time": time.time(), "role": role})
        print(f"[EVENT] Agent ended: {role}")

    print("Event handlers registered. Running crew...")
    result = monitor_crew.kickoff()
    time.sleep(0.5)
    print(f"\nTotal events captured: {len(events_log)}")
    print(f"Crew task output: {str(result)[:100]}")
    return events_log


if __name__ == "__main__":
    print("=== CrewAI Event Types Reference ===")
    for name, desc in EVENT_TYPES_REFERENCE:
        print(f"  {name:32s} -- {desc}")

    print("\n=== Live event bus demo ===")
    run_event_bus_demo()
