"""main -- run the full testing_and_training module end to end.

    python main.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from baseline_crew import run_baseline
from train_crew import run_manual_training_loop, show_train_signature, write_training_data
from baseline_crew import build_crew


def main() -> None:
    print("=== 1. Baseline crew (before training) ===")
    run_baseline()

    print("\n=== 2. Training data + crew.train() signature ===")
    write_training_data()
    show_train_signature()

    print("\n=== 3. Manual training loop (Groq, non-interactive) ===")
    crew = build_crew()
    run_manual_training_loop(crew, n_iterations=1)


if __name__ == "__main__":
    main()
