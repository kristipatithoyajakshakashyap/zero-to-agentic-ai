"""train_crew -- training data format, evaluation metrics, and a manual
non-interactive training loop that mirrors what crew.train() does under
the hood (crew.train() blocks on interactive human feedback per iteration,
which cannot run unattended, so this script shows the equivalent scored loop).

    python train_crew.py
"""

from __future__ import annotations

import inspect
import json
import sys
import time
from pathlib import Path

from crewai import Crew

from baseline_crew import build_crew, get_llm


def _kickoff_with_retry(crew: Crew, inputs: dict, max_retries: int = 4, base_delay: float = 8.0):
    """Run crew.kickoff() with backoff for Groq's tokens-per-minute rate limit."""
    for attempt in range(max_retries):
        try:
            return crew.kickoff(inputs=inputs)
        except Exception as exc:  # noqa: BLE001 - Groq rate limits surface as generic litellm errors
            if "rate_limit" in str(exc).lower() and attempt < max_retries - 1:
                delay = base_delay * (attempt + 1)
                print(f"  Rate limited, retrying in {delay:.0f}s...")
                time.sleep(delay)
                continue
            raise

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TRAINING_DATA = [
    {
        "input": {"topic": "reinforcement learning"},
        "expected_output": (
            "Reinforcement learning is a type of machine learning where an "
            "agent learns to make decisions by interacting with an "
            "environment and receiving rewards or penalties."
        ),
    },
    {
        "input": {"topic": "transformer architecture"},
        "expected_output": (
            "The transformer architecture is a neural network design based "
            "on self-attention mechanisms that process input sequences in "
            "parallel, forming the basis of models like BERT and GPT."
        ),
    },
    {
        "input": {"topic": "gradient descent optimization"},
        "expected_output": (
            "Gradient descent is an optimization algorithm that iteratively "
            "adjusts model parameters to minimize a loss function, with "
            "variants including SGD, Adam, and AdaGrad."
        ),
    },
]


def write_training_data() -> Path:
    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    training_file = data_dir / "crew_training_data.jsonl"
    with open(training_file, "w", encoding="utf-8") as f:
        for row in TRAINING_DATA:
            f.write(json.dumps(row) + "\n")
    return training_file


def compute_metrics(reference: str, output: str) -> dict:
    ref_words = set(reference.lower().split())
    out_words = set(output.lower().split())
    overlap = len(ref_words & out_words) / max(len(ref_words | out_words), 1)
    length_ratio = min(len(output), len(reference)) / max(len(output), len(reference), 1)
    composite = overlap * 0.5 + length_ratio * 0.5
    return {"word_overlap": round(overlap, 3), "length_ratio": round(length_ratio, 3), "composite": round(composite, 3)}


def show_train_signature() -> None:
    sig = inspect.signature(Crew.train)
    print(f"Crew.train() signature: {sig}")


def run_manual_training_loop(crew: Crew, n_iterations: int = 2) -> list[float]:
    """Non-interactive equivalent of crew.train(): run + score each example."""
    iteration_averages: list[float] = []
    for iteration in range(1, n_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")
        scores = []
        for idx, example in enumerate(TRAINING_DATA):
            result = _kickoff_with_retry(crew, example["input"])
            metrics = compute_metrics(example["expected_output"], str(result))
            scores.append(metrics["composite"])
            print(f"  Example {idx + 1}: composite={metrics['composite']:.3f} {metrics}")
            time.sleep(2)
        avg = sum(scores) / len(scores)
        iteration_averages.append(avg)
        print(f"  Iteration {iteration} average score: {avg:.3f}")
    return iteration_averages


if __name__ == "__main__":
    training_file = write_training_data()
    print(f"Training data written to: {training_file} ({len(TRAINING_DATA)} examples)")

    show_train_signature()

    crew = build_crew()
    averages = run_manual_training_loop(crew, n_iterations=1)
    print(f"\nScore trend across iterations: {averages}")
