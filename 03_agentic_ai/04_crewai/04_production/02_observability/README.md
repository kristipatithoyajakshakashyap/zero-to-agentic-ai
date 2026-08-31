# Module 02 - Observability

> **MLCourse - Production Readiness - Observability**

## Why this matters

When an agent crew misbehaves in production, "it printed some text" isn't
enough to debug it — you need to know which agent ran, for how long, and
in what order. CrewAI emits an event for every stage of execution (crew
started, agent started/ended, task started/ended) on a global event bus.
This module teaches you to listen to those events and turn them into
structured logs and timing data.

## What you'll learn

- Enable and configure CrewAI tracing
- Use event listeners to monitor crew execution in real time
- Integrate with OpenTelemetry for distributed tracing
- Inspect traces to debug agent behavior
- Set up monitoring dashboards

## Key concepts

- **Tracing**: recording the full execution path of a crew run
- **Event listeners**: callbacks that fire during crew execution
- **OpenTelemetry**: industry-standard distributed tracing protocol
- **Trace inspection**: reading and analyzing trace data
- **Monitoring**: real-time visibility into crew performance

## Contents

1. `event_listeners.py` - CrewAI event bus, event type reference, `@crewai_event_bus.on()` subscription against a live Groq crew
2. `timing_logger.py` - custom `BaseEventListener` subclass tracking per-agent/task durations, exports trace to `data/crew_trace.json`
3. `otel_integration.py` - OpenTelemetry integration pattern (reference), Python-logging-based listener, production observability checklist
4. `main.py` - runs the whole module end to end

Every file has a `python <file>.py` entry point and can be run standalone. LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable.

After this module, continue to `03_coding_agents_and_cli` for code execution.
