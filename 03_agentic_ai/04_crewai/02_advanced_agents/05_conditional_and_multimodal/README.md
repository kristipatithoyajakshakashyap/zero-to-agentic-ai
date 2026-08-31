# Module 05 - Conditional and Multimodal

> **MLCourse - Advanced Agent Features - Conditional and Multimodal**

Not every task runs unconditionally. ConditionalTask lets you branch based on
previous results, and multimodal agents let CrewAI work with images. This
module covers conditional execution and image-understanding agents.

## What you'll learn

- Use ConditionalTask to branch crew execution based on outputs
- Attach conditions that gate whether a task runs
- Configure a multimodal Agent to analyze images
- Combine conditional logic with multimodal capabilities

## Key concepts

- **ConditionalTask**: a task that only executes if a condition is met
- **Condition functions**: callables that inspect prior task output
- **Multimodal agents**: agents that process text and images together (`multimodal=True`)

## Beginner walkthrough

- `conditional_tasks.py`: think of `ConditionalTask` as an if/else for
  crews. One task classifies a review as positive/negative, then two
  "candidate" follow-up tasks are queued — but only the one whose
  condition function matches the classification actually runs. Try
  changing the sample reviews and watch which reply gets written.
- `multimodal_vision_agent.py`: gives an agent `multimodal=True` so it can
  look at an image URL inside a task, not just read text. This one file
  uses OpenAI instead of Groq — read the note at the top of the file for
  why (Groq simply doesn't offer a vision model on this account right
  now). Everywhere else in the course stays Groq-only.
- `main.py` runs both in order.

Run any file on its own with `python <filename>.py`, or the whole module
with `python main.py`.

## Contents

1. `conditional_tasks.py` - ConditionalTask, condition functions, branching (Groq)
2. `multimodal_vision_agent.py` - image-understanding agent (OpenAI -- see note below)
3. `main.py` - runs both sections in sequence

Every file runs standalone (`python <file>.py`); `main.py` runs the whole module.

**Provider note:** every other module in this course uses Groq only. This
module is the single exception: `multimodal_vision_agent.py` uses
`OPENAI_API_KEY` because Groq currently exposes no vision-capable chat model
on this account and has no image-generation API at all, so there is no Groq
path for image understanding. `conditional_tasks.py` still uses Groq as
usual. DALL-E-style image *generation* is out of scope for this lesson.

After this module, continue to `03_flows_and_orchestration` to learn CrewAI Flows.
