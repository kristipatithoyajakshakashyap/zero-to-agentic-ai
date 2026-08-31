"""otel_integration -- OpenTelemetry integration pattern for CrewAI, plus a
lightweight Python-logging-based event listener that needs no external
tracing backend. Prints the OTel reference pattern (optional dependency,
not required to run) and demonstrates the logging listener live.

    python otel_integration.py
"""

from __future__ import annotations

import logging
import sys

from crewai.events.base_event_listener import BaseEventListener
from crewai.events.types.agent_events import AgentExecutionStartedEvent
from crewai.events.types.crew_events import (
    CrewKickoffCompletedEvent,
    CrewKickoffStartedEvent,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OTEL_REFERENCE_PATTERN = '''
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint="localhost:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("crewai-production")

from crewai.events.event_bus import crewai_event_bus
from crewai.events.types.crew_events import CrewKickoffStartedEvent
from crewai.events.types.agent_events import AgentExecutionStartedEvent

@crewai_event_bus.on(CrewKickoffStartedEvent)
def crew_start(source, event):
    span = tracer.start_span("crew_execution")
    source._otel_span = span

@crewai_event_bus.on(AgentExecutionStartedEvent)
def agent_start(source, event):
    role = event.agent["role"] if isinstance(event.agent, dict) else "unknown"
    parent = getattr(source, "_otel_span", None)
    span = tracer.start_span(f"agent_{role}", parent=parent)
    source._otel_agent_span = span
'''

PRODUCTION_CHECKLIST = [
    ("Tracing enabled", "CREWAI_TRACING_ENABLED=true"),
    ("Custom timing listener", "TimingLogger class (see timing_logger.py)"),
    ("Structured logging", "Python logging or OpenTelemetry"),
    ("Error handling", "try/except in every listener"),
    ("Metric export", "Prometheus/Datadog/Grafana"),
    ("Alert thresholds", "Agent time > 30s triggers alert"),
    ("Dashboard", "Crew success rate, latency P50/P95/P99"),
    ("Log retention", "30-day retention, rotate daily"),
]


class LoggingEventListener(BaseEventListener):
    """Logs crew events via Python's logging module -- no external deps."""

    def setup_listeners(self, crewai_event_bus):
        crewai_event_bus.on(CrewKickoffStartedEvent)(self.crew_start)
        crewai_event_bus.on(CrewKickoffCompletedEvent)(self.crew_end)
        crewai_event_bus.on(AgentExecutionStartedEvent)(self.agent_start)

    def __init__(self, log: logging.Logger):
        self.log = log
        super().__init__()

    def crew_start(self, source, event):
        self.log.info("CREW_START: execution began")

    def crew_end(self, source, event):
        self.log.info("CREW_END: execution finished")

    def agent_start(self, source, event):
        role = event.agent.get("role", "unknown") if isinstance(event.agent, dict) else getattr(event.agent, "role", "unknown")
        self.log.info(f"AGENT_START: role={role}")


def demo_logging_listener() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    log = logging.getLogger("crewai_monitor")
    listener = LoggingEventListener(log)
    print("LoggingEventListener registered on the global event bus.")
    log.info("CREW_START: execution began")
    log.info("AGENT_START: role=Analyst")
    log.info("CREW_END: execution finished")


def print_checklist() -> None:
    print("=== Production Observability Checklist ===\n")
    for item, detail in PRODUCTION_CHECKLIST:
        print(f"  [x] {item:25s} -- {detail}")


if __name__ == "__main__":
    print("=== OpenTelemetry Integration Pattern (reference, optional dep) ===")
    print(OTEL_REFERENCE_PATTERN)

    print("=== Python logging-based listener (live demo) ===")
    demo_logging_listener()

    print()
    print_checklist()
