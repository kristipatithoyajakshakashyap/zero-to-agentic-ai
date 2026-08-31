# Module 08: Advanced Reasoning Patterns

> **MLCourse - Agentic AI - LangGraph**

Four ways an agent can think — ReAct, Reflexion, Plan-and-Execute, and ReWOO — built from scratch in LangGraph, then benchmarked against each other on one shared task with real measured numbers.

## The concept

Module 02 taught you the ReAct loop:

```
loop:
    THINK   -> reason about what to do next
    ACT     -> call a tool
    OBSERVE -> append the result to the conversation
until the model answers instead of calling a tool
```

ReAct is the right default for most agents. But it has four structural weaknesses, and each of the other patterns in this module exists to fix one of them:

| Weakness of ReAct | What goes wrong | Pattern that fixes it |
|---|---|---|
| **No global plan** | Greedy and myopic; can't parallelise, can't be reviewed before it runs | Plan-and-Execute, ReWOO |
| **No learning from failure** | A retry is statistically identical to the first attempt | Reflexion |
| **Quadratic token waste** | Step *k* resends everything from steps 1..k-1 | ReWOO |
| **No separation of concerns** | One call plans, acts and answers — so no cheap executor, no cacheable plan | Plan-and-Execute, ReWOO |

## Why it matters

The difference between these patterns is not academic — it is measured in money, seconds and correctness. On the shared task in notebook 05, the four patterns spanned a **7.3x range in token cost** and a **6.9x range in latency** while all four produced the correct answer. Picking the wrong one for your workload is a real and recurring cost.

It matters in the other direction too. ReWOO is dramatically cheaper, but it physically cannot branch on what it discovers. Reflexion can rescue a task ReAct fails at, but only if you can verify the answer objectively — with a self-grading LLM it just spends triple the tokens for the same output. These are engineering trade-offs with rules, not a leaderboard.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_beyond_react](01_beyond_react.ipynb) | Instrument a ReAct agent and **measure** its four weaknesses, including the real per-call token growth |
| 02 | [02_reflexion](02_reflexion.ipynb) | Actor → evaluator → self-reflection, with lessons carried into the retry so failures accumulate as memory |
| 03 | [03_plan_and_execute](03_plan_and_execute.ipynb) | Planner writes the full plan up front, executor runs one step at a time, replanner adapts |
| 04 | [04_rewoo](04_rewoo.ipynb) | Plan with variable substitution, an LLM-free worker, one solver pass — the token-efficiency argument made concrete |
| 05 | [05_choosing_a_pattern](05_choosing_a_pattern.ipynb) | All four on **one** shared task; measured tokens, latency and correctness; a decision procedure |

### Walkthrough

**01 — Beyond ReAct.** Builds a `Meter` class (tokens, LLM calls, tool calls, latency) and runs a standard `create_agent` ReAct loop on the shared task. Then it demonstrates each weakness rather than asserting it: the six independent lookups that ReAct is forced to serialise; two identical retries of a task it gets wrong, showing that attempt 2 learns nothing from attempt 1; and a per-call token table showing exactly how much of the bill is spent re-reading the agent's own transcript.

**02 — Reflexion.** The three-role loop, applied to a unit-conversion task the actor reliably gets wrong on the first try. The notebook is emphatic about the two things that make or break the pattern: the memory must be `Annotated[list, operator.add]` so lessons **accumulate** rather than overwrite, and the evaluator must be **grounded** — ours parses the number and diagnoses the specific 100x error, because an LLM asked "was that good?" always says yes. Ends with an A/B test running the actor with and without the accumulated lesson, plus a repeated-reflection detector for spotting a stuck actor.

**03 — Plan-and-Execute.** Planner, executor and replanner as separate nodes with separate prompts. Covers the two bugs everyone hits — forgetting `plan[1:]` (which loops on step 1 forever) and a replanner that never says ANSWER (fixed with `MAX_CYCLES` plus a `force_answer` node). Shows the plan as a **reviewable artifact** you could gate on with `interrupt()`, which is the natural bridge to module 04.

**04 — ReWOO.** The variable-substitution plan format (`#E1 = population[Tokyo]`), a worker with **zero LLM calls**, and a single solver pass. Runs ReAct on the same task in the same cell for a like-for-like comparison, then projects both cost curves out to 50 steps to show the gap widening rather than staying a constant factor. Includes a prominent pitfall note about **labelling the evidence table** — an unlabelled `#E1 = 13960000` genuinely produced a wrong answer during development, and the notebook explains why that failure is inherent to ReWOO's design. Closes with an honest account of what ReWOO cannot do: branch, loop, or react to what it finds.

**05 — Choosing a pattern.** All four patterns, one task, one model, one session, one deterministic grader. Prints the comparison table, relative cost and latency rankings, and cost-curve projections. Then a section on reading the results honestly (this task is small; Reflexion's cost is bimodal; latency tracks round trips; n=1), followed by a five-question decision procedure and notes on composing the patterns as subgraphs.

## Measured results

From a live run of `05_choosing_a_pattern.ipynb` (Groq `qwen/qwen3.8-27b`, six tool lookups plus one division, deterministic grader):

| Pattern | LLM calls | Tool calls | Total tokens | Latency | Correct |
|---|---|---|---|---|---|
| ReAct | 3 | 7 | 2,183 | 2.0s | YES |
| Reflexion | 3 | 7 | 2,183 | 2.1s | YES |
| Plan-and-Execute | 10 | 6 | 4,922 | 13.7s | YES |
| **ReWOO** | **2** | 6 | **670** | 4.4s | YES |

Success rate was 4/4 — this task is well within every pattern's ability, which is the point: on an easy task the patterns differ in **cost**, not correctness. ReWOO was **3.3x cheaper than ReAct** and **7.3x cheaper than Plan-and-Execute** in tokens. Reflexion tied ReAct exactly because its actor passed on attempt 1, so no reflection was needed — a good illustration that Reflexion costs nothing extra when it isn't needed and roughly *n* times ReAct when it is.

Latency does not track tokens: ReAct was fastest despite three calls, because the pacing sleeps and larger `max_tokens` in ReWOO's two calls dominated at this small scale. Numbers are regenerated on every run and will vary.

## How to run

1. Put a Groq key in `03_agentic_ai/.env`:
   ```
   GROQ_API_KEY=gsk_...
   ```
   Every notebook walks up the directory tree to find that file, so it works from any working directory.
2. Run the notebooks in order (01 → 05).

**Models.** Groq (`qwen/qwen3.8-27b`) is primary; a local Ollama server (`llama3.1:8b` at `localhost:11434`) is the fallback if no key is present. OpenAI is never used.

**Rate limits.** Groq's free tier is roughly 8000 tokens per minute. Every model call goes through a `safe_invoke` helper that paces requests and backs off exponentially on HTTP 429, and notebook 05 adds an 8-second cool-down between patterns. Notebook 05 is the heaviest (roughly 18 model calls); if you re-run it back to back, give it a minute in between.

**Reproducibility.** No numbers in any notebook are hard-coded — every table is computed from that run's own meters, so your figures will differ from the ones above.

## Prerequisites

- [01_graph_basics](../01_graph_basics/README.md) — `StateGraph`, conditional edges, and state reducers (Reflexion's memory is a reducer)
- [02_tool_using_agents](../02_tool_using_agents/README.md) — **required**; `02_react_agent_loop` is the baseline this entire module measures against
- [04_human_in_the_loop](../04_human_in_the_loop/README.md) — notebook 03 shows where `interrupt()` would gate a proposed plan
- [06_multi_agent_systems](../06_multi_agent_systems/README.md) — the actor/evaluator and planner/executor splits are role-separation ideas you first met there
- [07_subgraphs_and_composition](../07_subgraphs_and_composition/README.md) — the hybrids in notebook 05 (Reflexion around ReWOO, ReAct executors inside a plan) are subgraph compositions

## What you'll learn

- How to instrument an agent so pattern choice becomes a measurement rather than an opinion
- Why ReAct's input cost grows quadratically, and what that means at 25 or 50 steps
- How to build a Reflexion loop whose reflections actually change the retry — and why the evaluator, not the reflector, is the hard part
- How to split planning from execution, and why the replanner is what keeps the pattern from being a brittle script
- How variable-substitution plans let a worker run tools with no model at all
- A decision procedure for picking a pattern, and how to compose patterns rather than choose between them

## Next

**[09_travel_planner](../09_travel_planner/README.md)** — the capstone, where these reasoning patterns and the composition techniques from module 07 come together in a full application.
