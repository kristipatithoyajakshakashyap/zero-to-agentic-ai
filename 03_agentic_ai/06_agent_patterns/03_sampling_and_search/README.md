# Module 03: Sampling and Search

> **MLCourse - Agentic AI - Agent Patterns**

Every technique in this module spends more LLM calls to buy more accuracy. That is the entire idea, and it is only a good idea when you can show it actually worked. This module builds the techniques and then measures them — including the honest cases where they do not help.

## The concept

```
   SELF-CONSISTENCY          sample N complete answers, vote on the majority
   TREE-OF-THOUGHTS           branch into partial approaches, evaluate, prune, go deeper on survivors
   ACCURACY-VS-COST CURVE     both of the above, at every N, with tokens and latency measured
```

Both techniques depend on the same raw material: **temperature-induced variance**. At `temperature=0` there is only one reasoning path, so there is nothing to vote on and nothing to branch from. Module 01 establishes the variance; modules 02-03 spend it; module 04 draws the resulting trade-off as a curve.

## Why it matters

Self-consistency and Tree-of-Thoughts are widely cited and easy to over-apply. On an easy task set, sampling five times can cost 5x the tokens for a measured **zero** point improvement — because there is no error left for a vote to correct. On a task with a real verifier, best-of-n with verification often beats a full tree search for less machinery. The only way to know which situation you are in is to measure on your own task, which is what every notebook here actually does before drawing a conclusion.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_temperature_and_variance](01_temperature_and_variance.ipynb) | What temperature does to the token distribution; measured diversity at three temperatures; the format-vs-reasoning asymmetry |
| 02 | [02_self_consistency](02_self_consistency.ipynb) | Sample N, vote on the majority; measured accuracy at N=1..5; the free confidence signal in the vote spread |
| 03 | [03_tree_of_thoughts](03_tree_of_thoughts.ipynb) | Branch / evaluate / prune, grounded by a deterministic checker, on a small Game-of-24 variant |
| 04 | [04_accuracy_vs_cost](04_accuracy_vs_cost.ipynb) | Accuracy, tokens and latency together, across N=1..7, with an honest read of the resulting curve shape |

### Walkthrough

**01 — Temperature and variance.** Explains temperature as scaling the logits before softmax, then measures it: five samples each at T=0.0, 0.7 and 1.2 on one task, counting distinct final answers versus distinct reasoning texts. The reasoning varies far more than the answer even at moderate temperature — that gap is what self-consistency exploits. Closes with the practical rule that gets reversed constantly in practice: low temperature for structured output and tool arguments, moderate temperature for anything you intend to sample more than once, and a demonstration that `temperature=0` is *not* byte-identical across calls.

**02 — Self-consistency.** The full algorithm in about ten lines: draw N samples once, then evaluate majority voting at every smaller N by taking prefixes — so the notebook measures five operating points from one set of calls. Reports measured accuracy at each N against a fixed baseline (a single sample at the *same* temperature, not at T=0), and is explicit when the technique buys nothing on an easy task set. Introduces the vote **agreement ratio** as a free confidence signal for routing, with the accompanying warning that unanimity measures stability, not truth — correlated model errors are unanimous errors.

**03 — Tree-of-Thoughts.** Branch / evaluate / prune on a small Game-of-24-style arithmetic puzzle, chosen because candidate expressions can be verified deterministically with `eval()` — which the notebook builds and tests *before* trusting it. Compares an LLM-as-judge evaluator against the deterministic checker on the same candidates to show why grounding the evaluator is the entire ballgame. Ends by running the same puzzle through a single pass, sample-4-keep-any-valid, and the full tree search, and states plainly that when a verifier exists and the search is shallow, best-of-n with verification is often simpler and cheaper than a tree.

**04 — Accuracy vs. cost.** A measurement harness recording accuracy, input+output tokens, and wall-clock latency together across N=1..7 on a four-task set (28 calls total). Draws the curve, computes marginal gain per extra sample, and names the three possible shapes a curve can take — rising-then-flat, flat-at-ceiling, flat-below-ceiling — with a different correct conclusion for each. Separates the three currencies a sampling decision spends (tokens, latency, rate-limit budget) and notes that concurrency only fixes the second one. Closes with a measured summary table and an operating-point recommendation table keyed to product situation, not to technique preference.

## How to run

```bash
.venv/Scripts/python -m jupyter lab
```

or headlessly with `nbclient`:

```python
import nbformat
from nbclient import NotebookClient

nb = nbformat.read("02_self_consistency.ipynb", as_version=4)
NotebookClient(nb, kernel_name="python3",
               resources={"metadata": {"path": "."}}).execute()
nbformat.write(nb, "02_self_consistency.ipynb")
```

Every notebook shares one small task set of six exactly-checkable word problems, defined inline (not a separate file, since it is short and used with minor variations across notebooks). Because this module samples repeatedly by design, it is the most call-hungry in the track — the shared `chat()` helper's pacing and 429 backoff matter most here.

### Model and keys

**Groq** (`qwen/qwen3.8-27b`) via `ChatGroq`, `GROQ_API_KEY` from `03_agentic_ai/.env`. OpenAI is never used. Notebook 04 alone makes 28 paced calls in one run; run modules sequentially rather than in parallel with other Groq-heavy work if you are sharing a free-tier key.

## Prerequisites

| Module | Why |
|---|---|
| [01_context_engineering](../01_context_engineering) | Token measurement conventions this module reuses |
| [02_langgraph/08_advanced_reasoning_patterns](../../../02_langgraph/08_advanced_reasoning_patterns) | Plan-and-execute and ReWOO — the non-branching cousins of Tree-of-Thoughts |

## Measured results

From a live run of this module (Groq `qwen/qwen3.8-27b`), exact figures are printed inside each notebook's own cells rather than restated here, since they are measured live and vary run to run — see the "MEASURED, this run" lines in notebooks 01, 02 and 04, and the accuracy/tokens/latency table at the end of notebook 04 for the headline numbers.

## Recap

| Idea | Takeaway |
|---|---|
| Variance is the raw material | No variance at T=0, nothing to vote on or branch from |
| Vote on normalised answers | Or votes never converge |
| Ground the evaluator | Deterministic > rubric > "is this good?" (never) |
| Measure three currencies | Accuracy, tokens, latency — together, not separately |
| Report null results | "+0 points for 5x cost" is a real and valid finding |

**Next module:** [04_self_critique](../04_self_critique) — instead of sampling more answers, make the model improve the one it already has.
