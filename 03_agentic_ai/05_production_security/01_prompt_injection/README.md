# Module 01 - Prompt Injection & Adversarial Attacks

> **MLCourse - Agentic AI - Production Security - Prompt Injection**

Prompt injection is the single most important security risk for LLM
applications and agents. This module explains the attack classes, why
simple mitigations fail, and how to defend at the system boundary.

## What you'll learn

- Why prompt injection is dangerous (instruction override + tool abuse)
- Direct injection and the instruction-override problem
- Indirect injection through documents and tool output
- Prompt extraction / system-prompt leaking
- Jailbreaking and adversarial framing
- Why static prompt rules are not a defense
- A working injection detector built without an API key

## Key concepts

- **Direct injection**: attacker instructions in the user message
- **Indirect injection**: attacker instructions hidden in retrieved content
- **Prompt extraction**: tricking the model into revealing its system prompt
- **Jailbreaking**: reframing to bypass restrictions
- **Boundary defense**: classify input, gate tool actions

## Contents

1. `01_prompt_injection.ipynb` - attack taxonomy, demonstrations, mitigation
   and a lightweight heuristic injection detector

After this module, continue to `02_guardrail_frameworks` to build the
deterministic checks that stop these attacks.
