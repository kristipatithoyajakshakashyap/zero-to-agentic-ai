# Module 07: LLM as Judge

> **MLCourse - Agentic AI - Agent Patterns**

This course has already *used* an LLM judge twice - in
[`03_rag_advanced/10_rag_evaluation`](../../03_rag_advanced/10_rag_evaluation) and in
[`06_multi_agent_debate`](../06_multi_agent_debate). Neither time did anyone ask the
obvious question: **is the judge any good?** This module answers it, with numbers.

## What the concept is

An LLM judge is a model asked to **score or compare** outputs instead of producing
them. It is the only practical way to evaluate open-ended text at volume - humans are
too slow and too expensive, exact-match metrics cannot read.

It is also a **measuring instrument**, and an uncalibrated instrument is not a
measurement, it is a number.

```
POINTWISE                              PAIRWISE
 one output at a time                   two outputs, head to head
 "score this 1-5 on correctness"        "which is more correct, A or B?"
   + absolute, comparable over time       + easier for a model to do well
   + cheap: N calls for N outputs         + no scale drift
   - scale drift, score clustering        - O(N^2) for a full ranking
   - very sensitive to the rubric         - POSITION BIAS
```

## Why it matters

- Judges silently decide which system version ships. A biased judge does not throw an
  error; it hands you a confident leaderboard.
- Three of its defects are measurable in a few dozen calls: **position bias**,
  **verbosity bias**, **self-preference**. There is no excuse for not measuring them.
- Optimising against a biased judge creates the bias as a *target*: a system tuned
  against a verbose-biased judge learns to pad.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_rubrics_and_pointwise](01_rubrics_and_pointwise.ipynb) | Vague vs anchored vs reference-based rubrics, measured separation |
| 02 | [02_position_bias](02_position_bias.ipynb) | Swap the order, measure the flip rate - on easy and on close pairs |
| 03 | [03_self_preference_and_verbosity](03_self_preference_and_verbosity.ipynb) | The two biases swapping does not fix |
| 04 | [04_calibrating_against_humans](04_calibrating_against_humans.ipynb) | Against the human labels from `03_rag_advanced/10_rag_evaluation` |

The evaluation pairs are hand-built: five questions each with a good answer and a
**wrong-for-a-stated-reason** answer (photosynthesis reversed, 404 described as 503,
list append as O(n), mRNA described as live-attenuated, rebase described as merge).
You cannot measure a judge without ground truth *about the judge*.

### Walkthrough

**01 - Rubrics and pointwise scoring.** Starts with the rubric everyone writes first
("rate this 1-5 for quality") and then an anchored one that names a single dimension
and describes every scale point, then a reference-based one.

**Measured:**

| rubric | mean good / mean bad | separated | gap |
|---|---|---|---|
| vague ("quality 1-5") | 5.00 / 1.00 | **4/5** | 4.00 |
| anchored (correctness) | 5.00 / 1.20 | **5/5** | 3.80 |
| reference-based | 5.00 / 1.00 | **5/5** | 4.00 |

Reported honestly: on *these* pairs the vague rubric separated nearly as well,
because the bad answers are flagrantly wrong - and it produced **one unparseable
verdict**, which the notebook records as missing data rather than quietly scoring it
3. The anchored rubric's win is that it separated **5/5** and used the scale for a
stated reason you could defend. The lesson is the failure mode to watch for: score
clustering and grade inflation, which appear as soon as the bad answers are fluent
rather than absurd.

**02 - Position bias.** The test every judge should be given: ask twice with the
answers swapped, and count how often the verdict follows the *slot* rather than the
*content*.

**Measured:**

| pair set | n | judge calls | **flip rate** | slot A chosen |
|---|---|---|---|---|
| easy (one answer plainly wrong) | 5 | 10 | **0%** | 0 both-times |
| **close quality (both correct)** | 3 | 6 | **33%** | **67% of verdicts** |

That contrast is the entire point. On easy pairs the judge looks flawless; on pairs
that are close in quality - **which is what your real evaluations always are**, since
you are comparing v1 against v2 of your own system - it flipped on one of three and
chose slot A in 4 of 6 verdicts. The notebook then implements the standard
mitigation: `judge_pair_symmetric` runs both orders and records a **tie** when they
disagree, because a tie is honest and picking one order's answer is not.

**03 - Self-preference and verbosity.** The two biases that survive swapping,
because they are about content.

**Verbosity, n=3 content-matched pairs** (same facts, one short, one padded with true
but unrequested material; positions swapped so position bias cannot contaminate it):

| rubric | long preferred | short preferred | tie / flipped |
|---|---|---|---|
| generic "more correct" | **2/3 = 67%** | 0/3 = 0% | 1/3 |
| with anti-padding clause | 1/3 | 1/3 | 1/3 |

Chance is 33/33/33. The generic judge preferred the longer answer **67%** of the
time despite the two stating identical facts - and note the generic prompt already
said "ignore length", which bought nothing. Adding an explicit clause ("unrequested
background does not improve an answer and may bury the point") moved it to 1/1/1. The
most reliable fix is not in the judge at all: **cap length in the generator's
prompt** so candidates are length-matched before the judge sees them.

**Self-preference, n=3** (model grades its own answer against a human-written one,
positions swapped): preferred **its own 1/3 (33%)**, the human **0/3 (0%)**, and was
**inconsistent on 2/3**. The notebook states the caveats next to the number rather
than after it: n=3 has an enormous interval, the model's answers may genuinely be
better, and same-model/same-prompt is the *weakest* version of this effect. The
practical rule stands regardless: **do not grade your own model's output with your
own model** when the result drives a decision.

| Bias | Survives swapping? | Practical fix |
|---|---|---|
| Position | No | Swap and require agreement; record ties |
| Verbosity | Yes | Score a named dimension; anti-padding clause; cap generation length |
| Self-preference | Yes | A different model family as judge, or humans on a sample |
| Score clustering | Yes | Anchored rubric; pairwise instead of pointwise |

**04 - Calibrating against humans.** Loads
[`../../03_rag_advanced/10_rag_evaluation/human_eval_results.json`](../../03_rag_advanced/10_rag_evaluation/human_eval_results.json) -
five RAG answers scored 1-5 on four dimensions by three graders - and runs our judge
over the same five items with the same rubric.

**Measured:**

| item | human | judge | diff |
|---|---|---|---|
| b769b2e4 | 3.67 | 4.50 | +0.83 |
| c81f0823 | 3.67 | 5.00 | +1.33 |
| 3b407e90 | 3.58 | 4.00 | +0.42 |
| 8ba4f184 | 3.08 | 2.00 | -1.08 |
| 09f13f3f | 3.50 | 4.00 | +0.50 |
| **mean** | **3.50** | **3.90** | |

- **MAE** on the 1-5 scale: **0.833**
- **Bias** (judge minus human): **+0.400** - the judge is systematically generous
- **Spearman rho: +0.975 (p = 0.005)**, Pearson r: +0.978 (p = 0.004)

Per dimension the picture is much worse than the headline correlation suggests:

| dimension | human mean | judge mean | diff |
|---|---|---|---|
| correctness | 3.67 | 4.20 | +0.53 |
| relevance | 3.80 | 4.20 | +0.40 |
| **completeness** | 3.47 | 2.20 | **-1.27** |
| **safety** | 3.07 | 5.00 | **+1.93** |

**And the caveat that dominates all of it:** the source file records
`inter_annotator_kappa = 0.0` - the three graders did not agree with each other
beyond chance. That is the human ceiling here. *If the humans do not agree, no judge
can be shown to agree with "the humans."* A rank correlation of +0.975 against labels
with zero inter-annotator agreement is a demonstration of the procedure, not a
validated judge, and the notebook says so rather than quoting the rho and moving on.

The disagreements are also instructive: most items are answers that **correctly
refuse** ("there is no mention of the Caterpillar in the provided context"). Whether
that scores high or low is a *rubric decision* - excellent on correctness and safety,
a failure on completeness - which is exactly how you get a kappa of 0.0. A large
judge-human gap is often evidence the rubric was underspecified **for the humans
too**.

The notebook closes with what a real calibration requires: 100+ items sampled from
real traffic, 3+ graders with kappa reported *first*, a held-out set if you tune the
judge prompt, both correlation and MAE, a re-run schedule pinned to the model
version, and a judge from a different model family than the generator.

## How to run

```bash
# from the repo root
.venv/Scripts/python -m jupyter lab   # or open the notebooks in VS Code
```

Run in order; each notebook is self-contained. Roughly 60 small Groq calls across
the module.

**Requirements**

- `GROQ_API_KEY` in `03_agentic_ai/.env` (the setup cell walks *up* to the folder
  containing `03_agentic_ai` and loads the `.env` inside it).
- `langchain-groq`, `scipy` (for `spearmanr`/`pearsonr` in notebook 04).
- Model: `qwen/qwen3.8-27b`. A local Ollama model works as a substitute if you swap
  the two lines in `make_llm`; there is deliberately no automatic fallback branch.
- Notebook 04 reads `03_rag_advanced/10_rag_evaluation/human_eval_results.json`,
  which is committed - you do not need to re-run that module first, though it helps
  to have read it.
- Groq free tier is 8000 TPM; every notebook sets `PACE = 2.0` and `safe_invoke`
  backs off exponentially on 429s.

## Prerequisites

| You should have done | Why |
|---|---|
| [`03_rag_advanced/10_rag_evaluation`](../../03_rag_advanced/10_rag_evaluation) | Where the human labels and the four dimensions come from; notebook 04 depends on its output file |
| [`06_multi_agent_debate`](../06_multi_agent_debate) | You already trusted a judge to pick a debate winner - this module is the audit |
| [`01_langchain/02_chat_models_and_prompts`](../../01_langchain/02_chat_models_and_prompts) | System prompts, temperature, and forcing a machine-readable output format |

## Where to go next

- [`../08_agent_benchmarks`](../08_agent_benchmarks) - deterministic graders,
  pass@k and run-to-run variance: what to do when you can avoid an LLM judge entirely.
  Prefer a checker over a judge whenever one exists.
- [`../../03_rag_advanced/10_rag_evaluation/02_ragas_framework.ipynb`](../../03_rag_advanced/10_rag_evaluation/02_ragas_framework.ipynb) -
  a judge-based metric suite you now know how to interrogate.
