# Module 09 - Prompt Optimization (DSPy)

> **MLCourse - Agentic AI - Agent Patterns**

## Concept

Every prompt you have hand-written in this course is a string you tuned by
eye. **DSPy** replaces that with a *program*: you declare typed inputs and
outputs (a **Signature**), supply a handful of labelled examples and a
**metric**, and an **optimiser** generates the prompt text for you - then
proves it helped with a number.

The mental shift is small but total: the prompt stops being source code you
edit and becomes a build artifact you compile, version, and re-compile when
the model or the task changes.

## Why it matters

- **Hand-tuning does not scale.** An agent with ten prompts is ten strings
  nobody dares touch.
- **"It reads better" is not evidence.** A metric turns prompt work into
  something you can defend in review and gate in CI.
- **Prompts are model-specific.** Swap the model and your careful phrasing
  is tuned for a model you no longer use. A compiled program is re-compiled
  in minutes.
- **House conventions cannot be guessed.** Your label taxonomy, your triage
  rubric, your tone rules - the model has never seen them. Examples teach
  them far more reliably than paragraphs of instructions.

### The measured result in this module

The running example is a support-desk triage task with an in-house priority
rubric that is deliberately *not* stated in the prompt. Same Groq model
(`qwen/qwen3.8-27b`), same signature, same held-out dev set - only the
generated prompt changes:

| | accuracy | correct |
|---|---|---|
| **Before** (zero-shot) | 66.7% | 8/12 |
| **After** (`BootstrapFewShot`) | 91.7% | 11/12 |
| **Delta** | **+25.0 pts** | **+3** |

Three fixes, zero regressions - all on the money-related rows where the
model's general intuition disagreed with the house rubric.

## Notebooks

### `01_dspy_basics.ipynb`
What a Signature is and why it replaces a prompt string. Pointing DSPy at
Groq through LiteLLM. `dspy.Predict` vs `dspy.ChainOfThought` as a one-word
change. Using `dspy.inspect_history()` to read the prompt DSPy actually
sent. Where DSPy sits next to LangChain / LangGraph / CrewAI.

### `02_signatures_and_metrics.ipynb`
Class-based signatures with `Literal` output types. `dspy.Example` and the
`.with_inputs()` call everyone forgets. Writing a metric and sanity-checking
the metric itself. A 429-safe evaluation loop, and the **baseline** score
that notebook 03 has to beat, plus an analysis of which rows the zero-shot
program gets wrong and why.

### `03_optimizing_with_dspy.ipynb`
The core notebook. What `BootstrapFewShot` really does (metric-filtered
self-generated few-shot examples). Compiling, re-scoring on the same held-out
set, and the row-by-row before/after diff. Reading the optimised prompt and
the demos baked into it. Saving the compiled artifact. When optimisation is
worth the tokens and when it is not.

### `04_shipping_optimized_prompts.ipynb`
Loading a compiled artifact back and the signature-drift trap. Composing
DSPy modules (`dspy.Module`, `named_predictors()`) so you can compile only
the weak link. Token accounting for what the compile actually cost. The
operational checklist: what invalidates an artifact, why the eval set lives
in the repo, and why you never hand-edit the compiled JSON.

## How to run

```bash
# from the repo root, with the project venv active
jupyter lab 03_agentic_ai/06_agent_patterns/09_prompt_optimization
```

Run the notebooks in order. Notebook 04 loads `triage_optimized.json`, which
notebook 03 writes - so run 03 before 04.

The generated files (`baseline_score.txt`, `triage_optimized.json`) are
written next to the notebooks and are safe to delete and regenerate.

## Prerequisites

- `GROQ_API_KEY` in `03_agentic_ai/.env`. The notebooks read it with a
  walk-up helper; note that the helper returns the **repo root**, so the
  path is `TRACK / "03_agentic_ai" / ".env"`.
- `dspy` (installed in the project venv). DSPy reaches Groq through LiteLLM
  using the `groq/` provider prefix - no OpenAI involved anywhere.
- Groq free tier is **8000 tokens/minute**. Every evaluation loop in this
  module paces itself and retries with exponential backoff on 429. Do not
  run these notebooks alongside other Groq-heavy work.

## Related modules

- `03_agentic_ai/06_agent_patterns/07_llm_as_judge` - what to do when your
  metric cannot be exact-match.
- `03_agentic_ai/06_agent_patterns/08_agent_benchmarks` - the same
  measure-before-you-claim discipline, applied to whole agents.
- `03_agentic_ai/04_crewai` and `02_langgraph` - the frameworks whose
  hand-written prompts this module argues against.
