# Module 08: Agent Benchmarks

> **MLCourse - Agentic AI - Agent Patterns**

How agent capability is actually measured, conceptually (tau-bench, GAIA,
SWE-bench - no downloads), then a tiny local benchmark harness you can run
yourself: a fixed task set, a deterministic grader, pass@k, and run-to-run
variance. The module's real lesson is not "how good is this agent" - it is
**how much you can trust the number you just computed**.

## What the concept is

A benchmark is four separable pieces:

```
TASK SET      fixed, versioned, small enough to run often
ENVIRONMENT   deterministic; same starting state for every attempt
AGENT         a function: task -> answer, instrumented for tokens and steps
GRADER        deterministic; NEVER shares code with the agent
```

If the grader lives inside the agent, or shares a normalisation function with it,
you are running a demo, not a benchmark. The three real-world benchmarks this
module studies each found a way to make grading deterministic - final database
state, quasi-exact string match, or an executed test suite - and **none of them
uses an LLM judge for its headline number**.

## Why it matters

- Every model release ships a benchmark table. This module is what makes those
  numbers legible instead of decorative.
- A single benchmark run is a **sample**, not a score. This module measures how
  large that sampling error actually is, on a real (if tiny) harness.
- It closes the loop on [`../07_llm_as_judge`](../07_llm_as_judge): prefer a
  deterministic checker over a judge whenever the task can be phrased that way.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_how_agents_are_measured](01_how_agents_are_measured.ipynb) | tau-bench, GAIA, SWE-bench explained conceptually - no downloads |
| 02 | [02_a_local_harness](02_a_local_harness.ipynb) | The four pieces, built at 1/1000 scale: 4 tasks, 2 tools, a ReAct-shaped agent |
| 03 | [03_pass_at_k](03_pass_at_k.ipynb) | The unbiased pass@k estimator; contrast with tau-bench's `pass^k` |
| 04 | [04_run_to_run_variance](04_run_to_run_variance.ipynb) | R repeated runs, the noise floor, and the smallest difference you can detect |

### Walkthrough

**01 - How agents are actually measured.** No datasets fetched, no code beyond
markdown. Explains three benchmarks by what they measure and, more importantly, by
**how their grader works**:

| | tau-bench | GAIA | SWE-bench |
|---|---|---|---|
| Task source | hand-written policy scenarios | hand-written questions | real GitHub issues |
| Environment | mutable database + tools | web + files | a repo in a container |
| Grader | **final DB state** | **quasi-exact match** | **the test suite** |
| Headline metric | `pass^k` (all k must succeed) | accuracy | resolved rate |
| Judge involved | no | no | no |

Flags the trap in the names: tau-bench's `pass^k` (pass-to-the-power-k) requires
**every** repeat to succeed and is pessimistic; `pass@k` (notebook 03) counts a
task solved if **any** of k attempts succeeds and is optimistic. Also flags SWE-bench
contamination (public repos a model may have memorised - hence SWE-bench Verified
and Live) and GAIA's private test-set answers, so quoted validation numbers are not
leaderboard numbers.

**02 - A local harness.** Builds the same four pieces at a scale you can run in
minutes: a 5-employee lookup world, two tools (`lookup`, `count_dept`), four graded
tasks (`salary`, `headcount`, `combined`, `compare`), and a capped 3-step ReAct-style
agent loop. Each task carries its own deterministic grader plus a `min_tools`
field used to flag **lucky guesses** - a pass with fewer tool calls than the task
genuinely requires.

**Measured** (temperature 0, run twice, identical):

| | score | tokens | tool calls | suspicious (guessed) |
|---|---|---|---|---|
| run 1 | 4/4 = 1.000 | 1644 | 6 | 0 |
| run 2 | 4/4 = 1.000 | 1644 | 6 | 0 |

Both runs identical, and the notebook says plainly what that does and does not
prove: with 4 tasks over 2 runs you cannot detect flakiness below roughly 12%,
so "identical" here is a statement about resolution, not about determinism. Cost is
reported too: **$0.000723/run**, scaling to $0.0723 for 100 runs - and a reminder
that a real task set (200 tasks x 5 repeats) is 250x this run's cost, which is why
people under-run benchmarks and why doing so is a real trade-off, not laziness.

**03 - pass@k.** Implements the unbiased Codex/HumanEval estimator
`pass@k = 1 - C(n-c, k) / C(n, k)` from n=3 samples per task at temperature 0.8 (so
attempts can actually differ), and sanity-checks it (`n=3, c=1` gives pass@1=0.333
but pass@3=1.000 - the value of retrying, made concrete).

**Measured**, n=3 samples/task, 4 tasks, T=0.8:

| task | n | c | pass@1 | pass@3 | answers seen |
|---|---|---|---|---|---|
| salary | 3 | 3 | 1.000 | 1.000 | 82000 |
| headcount | 3 | 3 | 1.000 | 1.000 | 3 |
| combined | 3 | 3 | 1.000 | 1.000 | 143000 |
| compare | 3 | 3 | 1.000 | 1.000 | Ana |
| **MEAN** | | | **1.000** | **1.000** | |

Every task passed every sample, so pass@1 = pass@3 = 1.000 and the pass@1->pass@3
gap the notebook is built to illustrate is **zero on this run** - reported honestly
rather than dressed up. The notebook explains what that means and does not mean: at
n=3 the only reachable per-task pass@1 values are {0, 1/3, 2/3, 1}, a coarse
instrument next to the n=10-100 used in published numbers, and it demonstrates the
estimator correctly without claiming to have measured this agent precisely. A worked
`0 < c < n` example is included so the mechanism is visible even where our own task
set didn't produce one.

**04 - Run-to-run variance.** R=3 identical repeats (T=0.8) of the same four tasks,
answering "how much does the score move when nothing changes?"

**Measured:**

| | value |
|---|---|
| scores per run | [1.000, 1.000, 1.000] |
| mean | 1.000 |
| std dev | **0.000** |
| tokens per run | 1644, 1644, 1644 (identical) |
| stable-pass / stable-fail / flaky tasks | 4 / 0 / 0 |
| distinct answers per task across runs | 1 each (82000, 3, 143000, Ana) |

The notebook refuses to oversell a clean zero: *"the sd came out 0.000... that does
NOT mean the agent is deterministic; it means 3 runs of 4 easy tasks did not sample
any of the variance. The honest statement is 'the noise floor is below the
resolution of this experiment', not 'there is no noise.'"* It then computes the
score granularity directly - **one task is 0.25 of this benchmark**, so no claimed
improvement smaller than 0.25 is expressible at all, regardless of variance - and
extrapolates the sample size a real claim needs:

| task count x runs | trials | detectable difference | verdict |
|---|---|---|---|
| 4 x 3 | 12 | 0.354 | too noisy |
| 20 x 5 | 100 | 0.122 | too noisy |
| 100 x 5 | 500 | 0.055 | too noisy |
| **200 x 10** | **2000** | **0.027** | **OK** for a 5-point claim |

This is the module's closing point: hundreds of tasks in real agent benchmarks are
not thoroughness for its own sake, they are the sample size a 5-percentage-point
claim actually requires - and this 4-task harness cannot support one.

### Reporting checklist (from notebook 04)

- [ ] task set version and count · [ ] model name, version, date · [ ] temperature
- [ ] R repeats, mean +/- sd (never a single run) · [ ] k and n for any pass@k
- [ ] tokens and cost per run · [ ] the per-task table · [ ] any excluded task, and why

## How to run

```bash
# from the repo root
.venv/Scripts/python -m jupyter lab   # or open the notebooks in VS Code
```

Run in order. Notebook 01 makes no Groq calls. Notebooks 02-04 make roughly
4 + 36 + 36 = 76 small, paced Groq calls in total (03 and 04 each sample 3x per
task across 4 tasks, capped at 3 agent steps).

**Requirements**

- `GROQ_API_KEY` in `03_agentic_ai/.env` (setup cell walks *up* to the folder
  containing `03_agentic_ai` and loads the `.env` inside it).
- `langchain-groq`. Model: `qwen/qwen3.8-27b`. A local Ollama model works as a
  substitute if you swap the two lines in `make_llm`; no automatic fallback branch
  exists on purpose.
- Groq free tier is 8000 TPM, shared with other work in this course. Notebooks
  02-04 set `PACE` (3.0-3.5s) between calls and `safe_invoke` backs off
  exponentially on 429s.

## Prerequisites

| You should have done | Why |
|---|---|
| [`../06_multi_agent_debate`](../06_multi_agent_debate) | Its n=4 head-to-head is exactly the kind of small-sample result this module tells you not to trust as-is |
| [`../07_llm_as_judge`](../07_llm_as_judge) | The judge-vs-checker trade-off this module resolves in favour of checkers wherever possible |
| [`../../02_langgraph/08_advanced_reasoning_patterns/01_beyond_react.ipynb`](../../02_langgraph/08_advanced_reasoning_patterns/01_beyond_react.ipynb) | The ReAct-shaped call/observe loop the harness's agent reuses |

## Where to go next

- Re-run [`../06_multi_agent_debate/04_when_debate_pays.ipynb`](../06_multi_agent_debate/04_when_debate_pays.ipynb)
  through this harness with R repeats if you want a trustworthy verdict on debate.
- [`../../03_rag_advanced/10_rag_evaluation/05_agent_trajectory_evaluation.ipynb`](../../03_rag_advanced/10_rag_evaluation/05_agent_trajectory_evaluation.ipynb) -
  grading the *path* an agent took, not just its final answer.
