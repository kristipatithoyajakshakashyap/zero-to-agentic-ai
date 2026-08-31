# Module 14: Async Human Approval

> **MLCourse - Agentic AI - Agent Patterns**

[`02_langgraph/04_human_in_the_loop`](../../02_langgraph/04_human_in_the_loop/README.md)
covered `interrupt()` with a human at the keyboard, answering in the very
next cell. This module is the far more common real case: the human is **not**
watching, and the approval might come back an hour, a day, or a week later
— from a completely different process than the one that asked.

## What the concept is

The pattern has four pieces, each demonstrated end to end with a fresh graph
and a genuinely separate reviewer path:

1. **A durable request**, written to a queue (a JSON file standing in for a
   real message queue or database table) — *before* the graph suspends, so a
   crash between the two never leaves an orphaned interrupt nobody can find.
2. **Suspension via LangGraph checkpointing** — the same `interrupt()` and
   checkpointer machinery from
   [`02_langgraph/03_persistence_checkpointing`](../../02_langgraph/03_persistence_checkpointing/README.md),
   which is what lets the asking process exit or crash without losing anything.
3. **A separate reviewer cell** that touches only the durable store — no
   shared Python state with the cell that asked — standing in for a
   dashboard running on someone else's machine, later.
4. **`Command(resume=...)` issued by a different invocation**, matched to the
   original thread purely by `thread_id`.

**No web server anywhere in this module** — that is deployment, and is
covered separately in this course's end-to-end projects. Everything here is a
JSON file and ordinary function calls, enough to demonstrate the pattern
faithfully without adding infrastructure that would obscure it.

## Why it matters

- Most real approvals — spend authorisation, legal sign-off, a deploy gate —
  represent genuine real-world latency. Modelling them as "the human is
  watching" is wrong from the start.
- The suspended thread has to **survive the asking process's death**, and the
  answer has to be able to **arrive from anywhere**. That is exactly what a
  checkpointer buys you, and this module is the payoff for the persistence
  work in `02_langgraph/03`.
- Real approval systems need timeout, escalation, and sometimes more than one
  signature — none of which a bare `interrupt()` gives you for free, and all
  three are built here from the same small set of primitives.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_approval_queue_and_suspension](01_approval_queue_and_suspension.ipynb) | Enqueue durably, suspend, resume from a genuinely separate cell, matched by `thread_id` |
| 02 | [02_timeout_and_escalation](02_timeout_and_escalation.ipynb) | Detecting an overdue request; reassigning (not duplicating) up an escalation chain |
| 03 | [03_multi_reviewer_signoff](03_multi_reviewer_signoff.ipynb) | N-of-M approval: a ballot box of independent votes gating a single resume |

### Walkthrough

**01 — Approval queue and suspension.** Builds a minimal durable
`ApprovalQueue`, a purchase-approval graph that enqueues *then* interrupts
(that order matters — reversing it risks a suspended thread with no
findable request), and proves durability by reading the queue back with a
brand-new `ApprovalQueue` object. The reviewer and resume functions are
written to read **only from disk**, never from earlier cells' variables —
the discipline that makes "separate process" more than a comment.

**02 — Timeout and escalation.** No checkpointer gives you a timeout signal;
a poller has to compute "overdue" from timestamps against an SLA. Escalation
**reassigns the same `request_id`** rather than creating a second one — a
duplicate risks two conflicting decisions racing with no defined winner — and
an exhausted escalation chain fails visibly instead of looping. Ends with a
composed `poll_cycle()`: escalate overdue requests, resume decided threads,
report what's still waiting — the shape a real scheduled job would run.

**03 — Multi-reviewer sign-off.** A single `interrupt()` cannot natively hold
"waiting on 2 of 3 people" — it fires once. The fix generalises notebook 01's
idea: a ballot box of independent per-reviewer votes, checked from outside
the graph, decides when to resume. Demonstrates **reject-fast** aggregation
(one rejection is immediately decisive, even with quorum-worth of approvals
still outstanding) and the honest edge case where a required reviewer's vote
is mooted by quorum before they ever cast it — a real product decision, not a
bug to hide.

## Prerequisites

- [`02_langgraph/03_persistence_checkpointing`](../../02_langgraph/03_persistence_checkpointing/README.md)
  — checkpointers and threads, used here without re-explanation.
- [`02_langgraph/04_human_in_the_loop`](../../02_langgraph/04_human_in_the_loop/README.md)
  — `interrupt()` and `Command(resume=...)` fundamentals with a human at the
  keyboard, which this module immediately generalises to a human who isn't.

## Providers and keys

**None.** All three notebooks are pure orchestration and state — no LLM calls
and no API key anywhere in this module. The subject is durable suspension and
resumption, not generation.

## Setup

```powershell
pip install langgraph langgraph-checkpoint-sqlite
```

Nothing else. No `.env`, no API key, no server process.

## Generated artifacts

Running the notebooks creates local JSON queue files and SQLite checkpoint
databases in this folder (`approval_queue.json`, `escalation_queue.json`,
`signoff_queue.json` and their matching `*_demo.db` / `async_approval.db`
files), each cleared at the start of its notebook for a reproducible run.
Safe to delete.

## Key takeaways

- Enqueue the durable request **before** calling `interrupt()`, never after —
  the ordering is what prevents an unfindable suspended thread.
- A checkpointer gives you indefinite, free suspension but **no timeout** —
  overdue detection is a policy your own poller computes from timestamps.
- Escalate by **reassigning** a request's id, never by duplicating it.
- For N-of-M approval, keep `interrupt()` firing once and move the "how many
  votes so far" logic into an external ballot box — the resume mechanism
  stays identical to the single-reviewer case.
- Decide your vote-aggregation rule (reject-fast vs. strict unanimity vs. true
  majority) deliberately — it silently defines what "approved" means.
