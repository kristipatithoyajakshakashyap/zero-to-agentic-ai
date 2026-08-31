# Module 05 - Security Evaluation & Red-Teaming

> **MLCourse - Agentic AI - Production Security - Security Evaluation**

Security work is incomplete without evaluation. A red-team suite runs a
battery of attacks against the agent and guardrails, measures how many are
caught, and tracks regressions over time. This module builds an automated
evaluation harness for prompt injection, guardrail coverage, cache safety,
and privacy -- without an API key.

## What you'll learn

- Why automated security evaluation matters
- Building a test suite of attack cases
- Measuring guardrail detection (recall, precision)
- Running a red-team loop against a guarded agent
- Cache and privacy regression checks
- Interpreting results and prioritizing fixes

## Key concepts

- **Recall**: fraction of attacks caught
- **Precision**: of what is blocked, how much is a real attack
- **False positives**: benign requests wrongly blocked
- **Regression testing**: run the suite in CI on every change
- **Scorecard**: track recall / fp / privacy-leak / cache-leak over time

## Contents

1. `01_security_evaluation.ipynb` - attack suite, guard evaluation,
   red-team harness, privacy + cache regression checks, security scorecard

This completes the Production Security sub-track. Review the earlier modules
(`01_prompt_injection` through `04_privacy_handling`) to season the defenses
before shipping an agent.
