"""main -- run the full observability module end to end.

    python main.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from event_listeners import run_event_bus_demo
from timing_logger import export_trace, run_timed_crew
from otel_integration import demo_logging_listener, print_checklist


def main() -> None:
    print("=== 1. Event bus + event types ===")
    run_event_bus_demo()

    print("\n=== 2. TimingLogger + JSON export ===")
    logger = run_timed_crew()
    trace_file = export_trace(logger)
    print(f"Trace exported to: {trace_file}")

    print("\n=== 3. OpenTelemetry pattern + logging listener ===")
    demo_logging_listener()

    print()
    print_checklist()


if __name__ == "__main__":
    main()
