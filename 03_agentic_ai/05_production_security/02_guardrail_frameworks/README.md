# Module 02 - Guardrail Frameworks

> **MLCourse - Agentic AI - Production Security - Guardrail Frameworks**

Guardrails are deterministic checks that sit between input, the model, and
the world. This module builds a modular guardrail pipeline -- input,
output, and action layers -- that fails closed, all without an API key.

## What you'll learn

- The layered guardrail architecture (input, output, action)
- Input guardrails: safety, relevance, format
- Output guardrails: schema validation with Pydantic
- Refusal detection and grounding / hallucination checks
- Deterministic fail-closed behavior
- Composing guardrails into a reusable pipeline
- Guarding tool calls before execution

## Key concepts

- **Fail closed**: deny by default on any check failure
- **Schema validation**: typed, validated structured output via Pydantic
- **Refusal guard**: detect model refusals / off-topic text
- **Grounding guard**: verify the answer stays in context
- **Action guard**: gate tool calls (parameters, policy) before running

## Contents

1. `01_guardrail_frameworks.ipynb` - layered architecture, Pydantic schema
   validation, refusal/grounding guards, tool action gating, and a composed
   guardrail pipeline

After this module, continue to `03_caching_strategies` to see how caching
interacts with (and must follow) guardrails.
