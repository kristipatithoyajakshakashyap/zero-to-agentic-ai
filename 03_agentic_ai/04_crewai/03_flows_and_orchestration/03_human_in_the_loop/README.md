# Module 03 - Human in the Loop

> **MLCourse - Flows and Orchestration - Human in the Loop**

Some decisions need a human. CrewAI Flows support @human_feedback to pause
execution and wait for human input, creating approval gates that keep humans in
control of critical steps.

## What you'll learn

- Use @human_feedback to pause and wait for human input
- Design approval gates for sensitive operations
- Collect structured feedback from humans
- Resume flows after human input
- Handle timeout and fallback scenarios

## Key concepts

- **@human_feedback decorator**: pauses flow until human provides input
- **Approval gate**: a checkpoint where humans approve or reject an action
- **Structured feedback**: collecting typed input, not just free text
- **Resume after feedback**: continuing flow execution with human input
- **Timeout handling**: what happens when humans do not respond

## Contents

1. `01_human_feedback.ipynb` - @human_feedback basics, input collection
2. `02_approval_gates.ipynb` - designing approval workflows, reject/modify
3. `03_timeout_and_fallbacks.ipynb` - handling no-response, defaults, retries

After this module, continue to `04_mcp_integration` for MCP server connections.
