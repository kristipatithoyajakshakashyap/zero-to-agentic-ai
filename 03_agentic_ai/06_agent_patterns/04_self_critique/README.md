# Module 04: Self-Critique

> **MLCourse - Agentic AI - Agent Patterns**

The model can improve its own output — but only if the critique loop is built correctly. Naive self-critique ("is this good? how could it be improved?") reliably produces sycophantic agreement and a revision that changes three words. This module builds the version that works: Constitutional AI, a written principle set the model critiques its output against and then revises to satisfy — and contrasts it directly with Reflexion, taught earlier in this course, which looks structurally identical but is grounded in something completely different.

## The concept

```
   REFLEXION (02_langgraph/08_advanced_reasoning_patterns/02_reflexion.ipynb)
   attempt -> EVALUATOR says the task FAILED -> reflect -> retry
                        ^ ground truth: a test, a checker, a computed answer

   CONSTITUTIONAL AI (this module)
   draft -> CRITIC says a PRINCIPLE was broken -> revise -> re-check
                        ^ ground truth: a document you wrote
```

Same loop shape. Different source of truth, and therefore different applicability. The one-line test that decides which one to use: **can a computer tell you the output is wrong?** Yes — Reflexion. No, but you can write down what "wrong" means — Constitutional AI.

## Why it matters

Teams reach for "self-reflection" as one undifferentiated idea, apply the wrong variant to their task, and get confused when it does not work — principle-based critique on a task with a single correct answer, or failure-based critique on a task with no way to fail. Constitutional AI's real value shows up only when the constitution is specific, checkable, prioritised and paired with remedies; a vague constitution produces a vague critique that changes nothing measurable, and this module proves that with objective checks rather than asking you to trust the model's self-report.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_the_critique_loop](01_the_critique_loop.ipynb) | The naive loop and its sycophancy failure, measured against a deterministic violation checker |
| 02 | [02_writing_a_constitution](02_writing_a_constitution.ipynb) | What makes a principle usable; priority ordering; testing a principle before trusting it |
| 03 | [03_constitutional_loop](03_constitutional_loop.ipynb) | The full bounded critique-revise loop, per-principle critique, oscillation detection |
| 04 | [04_constitutional_vs_reflexion](04_constitutional_vs_reflexion.ipynb) | Both patterns run on tasks the other one structurally cannot handle, then combined |

### Walkthrough

**01 — The critique loop.** Drafts a reply to an angry customer email, then runs the naive critique ("is this good? how could it be improved?") and measures the result with a deterministic `check()` function (internal-information leaks, overpromising language, word count, empathy markers) rather than trusting the model's account of its own improvement. The naive revision is typically more polished and barely changes the objective violation count — the central finding of the notebook. A crude fix (just naming five specific standards) closes much of the gap for the same number of calls, motivating the rest of the module.

**02 — Writing a constitution.** Four properties a principle needs to actually change behaviour: specific, checkable, narrow, actionable — with a bad/good example for each. Every principle is written as a `rule` (how to detect a violation) paired with a `fix` (what to do about it), because rules without remedies let revision drift toward whatever the model invents. Covers priority ordering (safety > truthfulness > helpfulness > style, always) and shows how to test a principle on two inputs where the answer is already known before trusting it on real drafts — plus how to spot overlapping principles that will fight each other during revision.

**03 — The constitutional loop.** Runs critique and revision end to end against the six-principle constitution from notebook 02: one critique call per principle (deliberately, since a single "check everything" call reliably finds two problems and stops), a revision instruction that includes "change nothing else" to keep the loop convergent, and a hard round cap. Measures objective violations round by round, reports the real call and token cost, and builds an oscillation detector — a principle that fires, clears, and fires again — using the deterministic checks rather than the LLM critique, since using the critic to audit itself would be circular. Closes with a gating pattern: run the free deterministic check on every draft, and spend the expensive LLM constitution only on drafts it flags.

**04 — Constitutional AI vs. Reflexion.** States the distinction four ways in a comparison table, then proves it by running each pattern on a task only it can handle: a verifiable arithmetic problem for Reflexion (where a written principle has nothing to check against) and an appropriateness judgement for Constitutional AI (where there is no ground truth to fail against — `reflexion_evaluate()` is written and shown to return `None` by necessity, not by omission). Ends with a combined-gate pattern used in real coding agents: correctness first via Reflexion-style verification, appropriateness second via a constitution, illustrated with SQL-injection code that passes a functional test and fails two principles no test would ever catch.

## How to run

```bash
.venv/Scripts/python -m jupyter lab
```

or headlessly with `nbclient`:

```python
import nbformat
from nbclient import NotebookClient

nb = nbformat.read("03_constitutional_loop.ipynb", as_version=4)
NotebookClient(nb, kernel_name="python3",
               resources={"metadata": {"path": "."}}).execute()
nbformat.write(nb, "03_constitutional_loop.ipynb")
```

All four notebooks share one situation (an angry customer, a cancelled order, an unapproved compensation policy) and one deterministic `check()` function, redefined inline in each notebook so each stands alone. Notebook 03 is the heaviest — six critique calls per round, up to three rounds, plus revisions.

### Model and keys

**Groq** (`qwen/qwen3.8-27b`) via `ChatGroq`, `GROQ_API_KEY` from `03_agentic_ai/.env`. OpenAI is never used. Notebook 04's Reflexion half computes its ground truth in Python (`TRUTH = 480 * 3 / 8 + 90 - 0.15 * 480`) rather than trusting an asserted answer, matching the pattern in `02_langgraph/08_advanced_reasoning_patterns/02_reflexion.ipynb`.

## Prerequisites

| Module | Why |
|---|---|
| [02_langgraph/08_advanced_reasoning_patterns/02_reflexion](../../../02_langgraph/08_advanced_reasoning_patterns/02_reflexion.ipynb) | **Read before notebook 04** — this module assumes you already know Reflexion and contrasts against it directly |
| [05_production_security](../../../05_production_security) | Guardrails, which enforce rules from outside the model rather than critique from within it |

## Recap

| Idea | Takeaway |
|---|---|
| "Is this good?" always says yes | Sycophancy is the default failure of naive self-critique |
| Rule + fix, always paired | A rule without a remedy lets revision drift |
| Priority order is mandatory | Safety > truthfulness > helpfulness > style |
| Measure with code, not the model | The critique's self-report of improvement is not evidence |
| Can a computer say it's wrong? | Yes -> Reflexion. No, but you can write the standard -> Constitutional AI |
| Use both, in order | Correctness gate first, appropriateness gate second |

## Track complete

| Module | What it gave you |
|---|---|
| [01_context_engineering](../01_context_engineering) | Measure, budget, trim and order the context window |
| [02_memory_at_scale](../02_memory_at_scale) | Survive a conversation that outgrows any budget |
| [03_sampling_and_search](../03_sampling_and_search) | Spend calls to buy accuracy — and measure whether it worked |
| [04_self_critique](.) | Make the model improve the answer it already has |
