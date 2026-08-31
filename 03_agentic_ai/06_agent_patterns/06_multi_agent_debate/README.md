# Module 06: Multi-Agent Debate

> **MLCourse - Agentic AI - Agent Patterns**

Two or more agents argue toward an answer and a judge decides. This is the pattern
you reach for when the failure mode is **"the model was confidently wrong and
nothing in the system noticed"** - and this module is as interested in when it does
*not* work as when it does.

## What the concept is

```
question
   |
   +--> AGENT A  (a persona: fast, direct)      -->  opening position
   +--> AGENT B  (a persona: sceptical)         -->  opening position
   |
   v
ROUND 2: each agent is shown the OTHER's argument and may revise or defend
   |
   v
 JUDGE reads both final positions and picks one
   |
   v
answer
```

Two things make this a debate rather than two samples:

1. **The debaters differ.** Same prompt, same temperature, same model = you paid
   twice for one opinion. Different personas (or ideally different models, tools or
   retrieved context) are what make disagreement possible.
2. **They see each other.** Round 2 carries the opponent's argument in context. That
   is the entire mechanism. Remove it and you have voting, not debate.

The claim under test is specific: *an error that survives one pass often does not
survive being contradicted in writing.* Whether that holds is empirical, and this
module measures it.

## Why it matters

- It is the standard answer to "how do I catch confident errors?" and it is
  routinely deployed without anyone checking that it helped.
- It has a **known, fixed cost** (~4-5x a single pass in tokens) and an **unknown,
  task-dependent benefit**. That asymmetry is the whole lesson.
- Understanding it teaches you to choose multi-agent architectures by **failure
  mode** rather than by architecture diagram - the comparison against supervisor
  and swarm in notebook 03.
- Its weakest link, the judge, is the subject of the next module.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_debate_basics](01_debate_basics.ipynb) | The propose / cross-examine / judge loop, one full transcript, what it cost |
| 02 | [02_aggregation_and_capitulation](02_aggregation_and_capitulation.ipynb) | Judge vs majority vote; measuring capitulation and rescue rates |
| 03 | [03_debate_vs_supervisor_and_swarm](03_debate_vs_supervisor_and_swarm.ipynb) | Explicit contrast with the LangGraph patterns; how to choose |
| 04 | [04_when_debate_pays](04_when_debate_pays.ipynb) | single vs self-consistency@3 vs debate on 4 graded tasks |

The task set is four questions with a single checkable numeric answer
(`bat_ball`, `widgets`, `strawberry`, `avg_speed`), and **the grader is
deterministic** - it parses the `FINAL: <number>` line. No LLM grades anything in
this module's measurements, so what is being measured is the method, not a judge.

### Walkthrough

**01 - Debate basics.** Builds the minimal loop and prints one complete transcript
on the bat-and-ball problem. The result is the honest one: **both agents answered
0.05 in round 1 and again in round 2 - they agreed from the start, so the debate
bought nothing.** The cost, however, was real and is reported:

| | calls | in | out | cost USD |
|---|---|---|---|---|
| single pass | 1 | 74 | 206 | 0.000143 |
| debate (2 rounds + judge) | 5 | 1191 | 324 | 0.000537 |

**5.4x the tokens** for the same answer. Note the multiplier exceeds the call-count
ratio, because rebuttal and judge prompts carry the whole transcript - debate is
quadratic-ish in transcript length, which is why real systems cap it at two rounds
and two agents.

**02 - Aggregation and capitulation.** Two aggregation strategies (a judge vs
majority vote over three temperature-0.9 samples), then the experiment that decides
whether debate can work at all: contradict the agent with a plausible wrong number
and see which way it moves.

**Measured, n=4 tasks:**

| | count | rate |
|---|---|---|
| correct on first pass | 2/4 | - |
| ...of those, **folded** when contradicted | 1 | **capitulation 50%** |
| wrong on first pass | 2/4 | - |
| ...of those, **fixed** when contradicted | 0 | **rescue 0%** |

Debate can only pay if rescue exceeds capitulation. On this task set it is
**NOT favourable** - the model is more likely to abandon a correct answer under
pressure than to repair a wrong one. That is the characteristic way debate makes
things worse, and it is measured here rather than asserted. (Four tasks is a tiny
sample; the notebook says so. The value is the *procedure*.)

Self-consistency is also shown failing informatively: on `avg_speed` the three
samples were `[2.0, 1.0, 120.0]` - only **1/3 agreement**, majority `2.0`, truth
`40`. Voting over correlated samples from one model cannot fix a systematic error.

The notebook closes with a one-question preview of position bias: the same
disagreement judged in both orders. Here the judge was **position-consistent**,
which module 07 shows is not something to count on.

**03 - Debate vs supervisor vs swarm.** The explicit contrast with
[`../../02_langgraph/06_multi_agent_systems`](../../02_langgraph/06_multi_agent_systems):

| | **Supervisor** | **Swarm** | **Debate** |
|---|---|---|---|
| Agents differ by | capability (tools, domain) | capability | **stance** (same capability) |
| Work is | divided | passed along | **duplicated on purpose** |
| Disagreement is | a bug | rare - one agent is active | **the entire point** |
| Buys you | coverage and tool access | continuity across domains | **error correction** |
| Fails when | the router mis-assigns | nobody hands off, or ping-pong | agents agree, or fold |

> Supervisor and swarm exist because **one agent cannot do all the work**.
> Debate exists because **one agent cannot check its own work**.

The same VAT-total problem is solved both ways and instrumented:

| pattern | result | calls | tokens | what it bought |
|---|---|---|---|---|
| supervisor | CORRECT | 2 | 461 | access to the catalogue |
| debate | CORRECT | 3 | 1334 | a second opinion |

Both are right; they remove **different risks**. Delete the catalogue from the
debate's context and no amount of arguing recovers it - two agents confidently
hallucinating prices produce a confident hallucinated total. Conversely a supervisor
cannot catch VAT applied to the wrong base, because nobody in that architecture is
asked to disagree with the maths specialist.

**04 - When debate pays.** The head-to-head, same tasks, same grader, same meter.

**Measured result:**

| method | correct | acc | calls | tokens | cost USD |
|---|---|---|---|---|---|
| single | 3/4 | 0.750 | 4 | 1163 | 0.000603 |
| self_consistency@3 | 3/4 | 0.750 | 12 | 3511 | 0.001823 |
| **debate** | **4/4** | **1.000** | 20 | 4849 | 0.001696 |

Relative to the single-pass baseline:

| method | acc delta | token mult | win / tie / loss |
|---|---|---|---|
| self_consistency@3 | +0.000 | 3.02x | 0 / 4 / 0 |
| debate | **+0.250** | **4.17x** | **1 / 3 / 0** |

Per task, the entire difference is one question:

| task | truth | single | self_cons@3 | debate |
|---|---|---|---|---|
| bat_ball | 0.05 | OK | OK | OK |
| widgets | 5 | OK | OK | OK |
| strawberry | 3 | OK | OK | OK |
| **avg_speed** | **40** | **2.0 X** | **3.0 X** | **40.0 OK** |

**Read that honestly.** Debate won one task out of four and lost none - encouraging,
and *not significant at n=4*. Three of the four tasks were solved by a single call,
so debate paid 4.17x the tokens for the same answer on 75% of the workload. Notably
self-consistency, at 3x the tokens, bought **nothing at all** here: three samples of
one model share a prior and therefore share its mistakes.

The interesting tension between notebooks 02 and 04 is left standing rather than
smoothed over: capitulation measurement says the arrow points the wrong way, and the
head-to-head says debate won a task. At these sample sizes both are consistent with
"we do not know yet". The correct next step is the same harness on 100+ real tasks -
which is what [`../08_agent_benchmarks`](../08_agent_benchmarks) is for.

### When debate is genuinely worth it

- The answer is checkable but only **expensively** (human review, a slow test suite)
  - debate is cheaper than the check and filters what reaches it.
- The task has a **known trap** a sceptic persona is primed to catch (`avg_speed` is
  exactly this).
- The agents **differ substantively** - different models, tools, or retrieved
  context. Two personas of one model at temperature 0 is the weakest form of debate
  there is, and it is what this module runs.
- A wrong answer costs much more than 5x an inference call.

### When it is not

- High-volume, low-stakes traffic - use [`../05_semantic_routing`](../05_semantic_routing).
- Tasks you cannot grade - you will never know whether it helped.
- Anywhere a **deterministic verifier** exists. A unit test, a schema check or a
  calculator beats any number of arguing language models - the same lesson
  [`../../02_langgraph/08_advanced_reasoning_patterns/02_reflexion.ipynb`](../../02_langgraph/08_advanced_reasoning_patterns/02_reflexion.ipynb)
  makes about evaluators.

## How to run

```bash
# from the repo root
.venv/Scripts/python -m jupyter lab   # or open the notebooks in VS Code
```

Run in order; each notebook is self-contained. Notebook 04 is the slow one -
roughly 36 paced Groq calls, a few minutes of wall clock.

**Requirements**

- `GROQ_API_KEY` in `03_agentic_ai/.env`. The setup cell walks *up* to the folder
  containing `03_agentic_ai` and loads `03_agentic_ai/.env` from there.
- `langchain-groq`. Model: `qwen/qwen3.8-27b`. A local Ollama model works as a
  substitute if you swap the two lines in `make_llm` - there is deliberately no
  automatic fallback branch, because a notebook that silently changes model
  produces numbers you cannot trust.
- Groq's free tier is 8000 TPM. Every notebook sets `PACE` (2.5 s, 4.0 s in
  notebook 04) between calls and `safe_invoke` backs off exponentially on 429s.
  Do not run several modules of this track at once.

## Prerequisites

| You should have done | Why |
|---|---|
| [`02_langgraph/06_multi_agent_systems`](../../02_langgraph/06_multi_agent_systems) | Supervisor and swarm - notebook 03 contrasts against them directly |
| [`02_langgraph/08_advanced_reasoning_patterns`](../../02_langgraph/08_advanced_reasoning_patterns) | Reflexion's lesson that an ungrounded evaluator is worth little |
| [`01_langchain/02_chat_models_and_prompts`](../../01_langchain/02_chat_models_and_prompts) | `ChatGroq`, system/user messages, reading `usage_metadata` |
| [`05_semantic_routing`](../05_semantic_routing) | The opposite trade - spend less - and the habit of measuring the ledger |

## Where to go next

- [`../07_llm_as_judge`](../07_llm_as_judge) - the judge you just trusted, taken
  apart: rubrics, position bias, self-preference, calibration against human labels.
- [`../08_agent_benchmarks`](../08_agent_benchmarks) - running this kind of
  comparison properly, with pass@k and run-to-run variance.
