# Module 04 - LLM Connections

> **MLCourse - Production Readiness - LLM Connections**

## Why this matters

CrewAI never talks to a model provider directly — under the hood it uses a
library called LiteLLM, which understands one naming convention
(`"<provider>/<model>"`) for dozens of providers. Once you understand that
convention, switching providers is a one-line change. This course
standardizes on **Groq** (fast, cloud, needs a free API key) as the
primary provider, with **Ollama** (free, runs on your own machine) as a
fallback if Groq is unreachable. We never use OpenAI in this course.

## What you'll learn

- The `"provider/model"` string format CrewAI's `LLM` class expects
- How to check whether Groq or Ollama is actually reachable before using it
- Temperature and `max_tokens` — what they control and when to change them
- How to build a small "pick the best available provider" strategy class

## Contents

1. **`provider_comparison.py`** — Side-by-side comparison of Groq vs.
   Ollama (cost, speed, quality, privacy, setup), live reachability
   checks for both, a real LLM call using whichever one is available, and
   a table of temperature/`max_tokens` presets for different task types.
2. **`llm_selection_strategy.py`** — `LLMSelectionStrategy`, a small class
   that scores each *reachable* provider and picks the best one for a
   given task (e.g. "high complexity" tasks weigh quality more, "prefer
   speed" weighs Groq's speed more). Ends with a production
   configuration checklist.
3. **`main.py`** — Runs both files above in order.

## How to run it

```bash
python provider_comparison.py
python llm_selection_strategy.py
python main.py   # runs everything in one go
```

**LLM provider:** Groq (`GROQ_API_KEY` in `03_agentic_ai/.env`), falling
back to local Ollama if Groq is unreachable. No OpenAI anywhere in this
module, by design.

After this module, continue to `05_capstone_full_stack_app_builder` for the capstone.
