"""run_pipeline -- runs the capstone pipeline end to end using the
Flow-based orchestration (parallel dev + routing), saves the output, and
scores it with the metrics module.

This is the file to run if you only have time for one script in this
module -- it demonstrates the full architecture in a single pass.

    python run_pipeline.py
"""

from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from flow_orchestration import run_flow_pipeline
from metrics import DEPLOYMENT_CHECKLIST, analyze_output


def run() -> None:
    print("=== Full-Stack App Builder Pipeline (Flow-based) ===")
    print("Stages: PM -> Architect -> [Frontend + Backend] -> QA -> (route) -> Writer\n")

    output = run_flow_pipeline()

    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    output_file = data_dir / "capstone_pipeline_output.txt"
    output_file.write_text(output, encoding="utf-8")
    print(f"\nFull output saved to: {output_file}")

    print("\n=== Output Quality Metrics ===")
    metrics = analyze_output(output, "Flow pipeline output")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    print("\n=== Production Deployment Checklist ===")
    for idx, item in enumerate(DEPLOYMENT_CHECKLIST, 1):
        print(f"  {idx:2d}. [ ] {item}")


if __name__ == "__main__":
    run()
