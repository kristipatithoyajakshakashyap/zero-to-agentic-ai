# Module 01 - Testing and Training

> **MLCourse - Production Readiness - Testing and Training**

## Why this matters

You wouldn't ship code without tests, and you shouldn't ship an agent crew
without evaluating its output either. CrewAI ships two ways to check
quality: `crewai test` (a quick CLI sanity check) and `crew.train()` (runs
the crew many times against reference examples and tunes prompts based on
how close the output gets). This module builds a tiny "summarize a topic"
crew and puts both mechanisms to work on it.

## What you'll learn

- Use `crewai test` to evaluate crew output automatically
- Train crews with `crew.train()` for iterative improvement
- Define evaluation metrics and benchmarks
- Compare crew runs and track improvement over time
- Debug failing evaluations

## Key concepts

- **crewai test**: CLI command for automated crew evaluation
- **crew.train()**: programmatic training loop for crew optimization
- **Evaluation metrics**: measuring output quality, relevance, accuracy
- **Benchmark runs**: comparing against expected outputs
- **Iterative improvement**: using evaluation results to refine crews

## Contents

1. `baseline_crew.py` - builds a minimal summarizer crew (Groq LLM) and runs it once to establish a baseline
2. `train_crew.py` - training data format, `crew.train()` signature, and a non-interactive manual training loop with evaluation metrics
3. `main.py` - runs the whole module end to end (baseline, then training loop)

Every file has a `python <file>.py` entry point and can be run standalone. LLM provider: Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling back to local Ollama if Groq is unreachable.

After this module, continue to `02_observability` for tracing and monitoring.
