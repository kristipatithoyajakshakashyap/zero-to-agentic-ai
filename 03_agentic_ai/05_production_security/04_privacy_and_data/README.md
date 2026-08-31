# Module 04 - Privacy & Data Handling

> **MLCourse - Agentic AI - Production Security - Privacy & Data Handling**

Agents process text that contains personally identifiable information
(PII). Sending raw PII to a model, logging it, or caching it creates privacy
and compliance risk. This module covers detecting and redacting PII before
it reaches an LLM, data minimization, and local-first privacy.

## What you'll learn

- What counts as PII and why it is risky in agent pipelines
- Detecting PII with deterministic pattern matching
- Redaction: masking PII before the model sees it
- Masking vs. removal
- Data minimization principles
- Local-first privacy (running models locally)
- Composing a privacy guard into the agent pipeline

## Key concepts

- **PII**: emails, phones, SSNs, addresses, names, account IDs
- **Redaction**: replace PII with `<EMAIL>`, `<PHONE>`, `<SSN>` tokens
- **Minimization**: send the least data needed for the task
- **Local-first**: keep data on your machine
- **Redact before**: logging, caching, external calls, prompt building

## Contents

1. `01_privacy_handling.ipynb` - PII detection, redaction, mask/remove,
   data minimization, local-first privacy, and a privacy guard pipeline

After this module, continue to `05_security_evaluation` to build an
automated red-team harness that measures how well these defenses work.
