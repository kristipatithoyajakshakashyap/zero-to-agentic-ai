# Module 10: State Migration and Versioning

> **MLCourse - Agentic AI - LangGraph**

[`03_persistence_checkpointing`](../03_persistence_checkpointing/README.md)
taught you to save graph state so a conversation survives a restart. This
module asks the question that follows once your agent has been in production
for more than a day: **what happens to the checkpoints already on disk when
you ship a new version of the graph?**

Checkpoints are data at rest. Data at rest outlives the code that wrote it. A
thread paused for human approval on Friday can get resumed on Monday by a
deployment that shipped over the weekend — with a `TypedDict` that no longer
matches what is stored.

## What the concept is

A LangGraph checkpoint is a **plain, untyped dict of channel values**. Nothing
validates it against the state class of the graph that loads it — the state
class only tells LangGraph which channels exist and how to merge writes into
them. That design is what makes checkpointing fast; it is also what makes
this module's whole subject possible.

This module works through the problem the way you would manage a database
migration, because it is the same problem:

1. **See it break.** Reproduce both failure modes on a real checkpoint store.
2. **Classify the change.** Which edits are safe, which are not, and which are
   dangerous precisely because they raise no error.
3. **Version the state and migrate it.** One small function per version step,
   run at the graph's entry.
4. **Recover what lazy migration cannot reach** — dormant threads, and threads
   suspended mid-`interrupt()`.

## Why it matters

- Every agent with a checkpointer is, whether you planned for it or not,
  running a system with **data that outlives its schema**.
- The failure is not hypothetical or rare: adding one field to a `TypedDict`
  and reading it without a default is enough.
- A **suspended** thread is the worst case, and the one classic
  database-migration guides do not cover: it holds a decision a human already
  made, so "just restart it" throws that decision away.
- The fixes are small and standard — a version stamp, a migration chain, an
  eager backfill — once you know to reach for them before shipping.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_when_the_schema_changes](01_when_the_schema_changes.ipynb) | What a checkpoint actually is; both failure modes, reproduced |
| 02 | [02_additive_vs_breaking_changes](02_additive_vs_breaking_changes.ipynb) | A taxonomy: safe changes, loud breaks, and silent data loss |
| 03 | [03_versioned_state_and_migrations](03_versioned_state_and_migrations.ipynb) | A version stamp, a migration chain, and the two ways to lose data anyway |
| 04 | [04_recovering_old_checkpoints](04_recovering_old_checkpoints.ipynb) | Bulk backfill, and repairing a thread suspended at `interrupt()` |

### Walkthrough

**01 — When the schema changes.** Opens a raw checkpoint and shows it is
`{'v', 'ts', 'id', 'channel_values', ...}` — no schema, no version, nothing
that says which `TypedDict` wrote it. Then reproduces both failure modes for
real: an existing thread's next turn raises `KeyError` on a field it never
had, and a thread suspended at a human-approval `interrupt()` cannot be
resumed *or* safely restarted, because restarting discards an approval a real
person already gave.

**02 — Additive vs breaking changes.** Runs four concrete edits against a
checkpoint from an older schema and records what actually happens. **Adding a
field, read with `.get(default)`, works.** Adding a field read with `state[…]`
raises a loud, useful `KeyError`. **Renaming a field produces no error at
all** — the old value sits orphaned in the database and the new field is
silently empty. Changing a reducer breaks even `get_state()`, because
inspecting the thread replays writes through the very reducer that is broken.
Ends with a PR checklist.

**03 — Versioned state and migrations.** Adds a `schema_version` field and a
migration chain (`v1→v2→v3`), installed as a node at `START` so every other
node can use direct `state[...]` access. The first, "obvious" version of the
migration node **loses the renamed field anyway** — not because the migration
function is wrong, but because the *graph's* state class no longer declares
the old channel, and separately because the *node's own annotation* filters
it again. Both are measured before the fix: declare the deprecated field as
`NotRequired[...]` on both the state class and the node signature during the
transition (**expand**), then drop it later (**contract**). Also proves
migrations must be idempotent, with a broken (list-appending) migration shown
alongside the correct one.

**04 — Recovering old checkpoints.** Enumerates every thread in a store with
`checkpointer.list(None)`, then runs a dry-run-first, per-thread-fault-
tolerant backfill that upgrades all of them and verifies the result. Then
tackles the case lazy migration cannot reach: `Command(resume=...)`
re-enters the interrupted node directly, bypassing `START` entirely. Measured:
attempting a resume on unrepaired state doesn't fail cleanly — the interrupt
is *consumed* before the node crashes, leaving the thread neither pending nor
retryable. The correct repair uses `update_state(..., as_node="migrate")`
*before* ever attempting a resume — `as_node` is what keeps the original
pending task (and the still-unclaimed interrupt) intact; omitting it would
have re-asked the human the question.

## Prerequisites

- [`03_persistence_checkpointing`](../03_persistence_checkpointing/README.md)
  — `MemorySaver`/`SqliteSaver`, threads, and what a checkpoint is for.
- [`04_human_in_the_loop`](../04_human_in_the_loop/README.md) — `interrupt()`,
  `Command(resume=...)`, and `update_state()`, all used here for repair rather
  than for the first time.

## Providers and keys

**None.** Every node in this module is an ordinary Python function returning a
dict. There are **no LLM calls anywhere in module 10** — the subject is state
plumbing, and a model would only add cost and noise to graphs that are
deliberately boring so the checkpoint behaviour is the only thing moving.

## Setup

```powershell
pip install langgraph langgraph-checkpoint-sqlite
```

Nothing else. No `.env`, no API key.

## Generated artifacts

Running the notebooks creates local SQLite files in this folder
(`migration_demo.db`, `taxonomy_demo.db`, `versioned_demo.db`,
`recovery_demo.db`) so each notebook starts from a clean, reproducible store.
Safe to delete.

## Key takeaways

- A checkpoint is an **untyped dict**. Nothing validates it against the
  schema that loads it, and nothing records which schema wrote it.
- **Additive** changes (new field + `.get(default)`) are safe. Renames,
  removals, and reducer changes are data migrations whether you treat them as
  one or not — and renames fail **silently**, which is worse than a crash.
- Put the version **in the state**, write **one migration function per step**,
  and run the chain as a node at `START` — but remember that both the graph's
  state class *and* that node's own annotation must still declare a
  deprecated channel during the transition, or the migration function never
  even sees the value it is supposed to carry across.
- **Lazy migration cannot reach a suspended thread**, and attempting a resume
  on one before repairing it can consume the pending interrupt and leave the
  thread permanently stuck. Repair with `update_state(..., as_node=...)`
  — choosing the right `as_node` is what preserves the original pending task
  — and always repair *before* the first resume attempt.
- Run an **eager backfill** for dormant and suspended threads: dry-run first,
  never let one bad thread abort the batch, and verify by re-scanning.
