# Module 07: Subgraphs and Composition

> **MLCourse - Agentic AI - LangGraph**

Building graphs out of other graphs — encapsulating a workflow behind a boundary, mapping state across that boundary, and fanning out to a number of branches you only discover at runtime.

## The concept

A compiled LangGraph is a `Runnable`, and `add_node` accepts any `Runnable`. That single fact is the whole subgraph API: build a graph, `compile()` it, and drop the result into a parent graph as one node.

That gives you two composition primitives, and they solve different problems:

| Primitive | Problem it solves | Branch count |
|-----------|-------------------|--------------|
| **Subgraph** — a compiled graph used as a node | Encapsulation, reuse, private state, isolated testing | Fixed at build time |
| **`Send`** — `from langgraph.types import Send` | Fan-out when you don't know how many branches until runtime | Decided at runtime |

## Why it matters

Every graph in modules 01–06 was flat: one state schema, one set of nodes, one compile. That works to roughly a dozen nodes and then fails in four specific ways:

1. **State-key collisions** — one namespace means two stages that both want `score` silently clobber each other.
2. **Untestable middles** — there is no runnable object for "the interesting part"; testing it means hand-building the entire upstream state.
3. **No reuse** — sharing logic with a second pipeline means copy-paste drift or a merged mega-graph.
4. **Coarse checkpoints** — the checkpointer stores one blob for the whole state, so resume and time-travel are all-or-nothing.

Composition fixes all four by introducing **boundaries**. The price you pay is that the boundary has to be crossed correctly — and that is where essentially every subgraph bug lives, which is why notebook 03 is dedicated to it.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_compose_graphs](01_why_compose_graphs.ipynb) | The four failure modes of a flat graph, demonstrated in running code; when a section deserves to be extracted |
| 02 | [02_building_a_subgraph](02_building_a_subgraph.ipynb) | Compile a child graph and use it as a node; run it standalone; stream with `subgraphs=True`; namespaced checkpoints; reuse in a second parent |
| 03 | [03_shared_vs_isolated_state](03_shared_vs_isolated_state.ipynb) | **The main pitfall.** The boundary filters by key *name* and never renames. Three failure demos plus the wrapper-function pattern that fixes them |
| 04 | [04_send_api_map_reduce](04_send_api_map_reduce.ipynb) | `Send(node, payload)` for runtime fan-out; per-worker schemas; the mandatory reducer; heterogeneous dispatch; an LLM-planned map-reduce |
| 05 | [05_composed_pipeline](05_composed_pipeline.ipynb) | Everything at once: two isolated subgraphs in a parent, one containing a `Send` fan-out, one containing a retry loop |

### Walkthrough

**01 — Why compose graphs.** Builds an eight-node document pipeline the naive way, then breaks it on purpose: a key collision that silently discards a score, a "test the middle" exercise that requires inventing five irrelevant keys, and a checkpoint dump showing one flat blob. Closes with a checklist for deciding what to extract.

**02 — Building a subgraph.** A three-node grader child with one private key, run standalone, then embedded in a parent with `add_node("grader", grader_app)`. Shows that the child's private key does *not* leak into the parent, draws the composed graph with and without `xray=1`, contrasts default streaming against `subgraphs=True`, inspects namespaced checkpoint history, and reuses the same compiled child in a second unrelated parent.

**03 — Shared vs isolated state.** The mental model first: the boundary runs two name-based filters and does no renaming. Then three failure demos — a loud `KeyError` from a mismatched input name, a **silent** loss from a mismatched output name (the dangerous one), and a reducer surprise where a shared `Annotated[list, operator.add]` turns assignment into accumulation. The fix is the wrapper-function pattern, shown minimal and then production-shaped with validation, error containment and output projection, and finally with a real LLM-backed translator child whose vocabulary shares nothing with its parent. Ends with a decision guide and a debug checklist.

**04 — The `Send` API.** Starts by showing why conditional edges cannot express runtime fan-out (they return names of nodes that must already exist). Introduces `Send`, the per-worker schema, and a live demonstration that omitting the reducer on the collector key raises rather than merges. Proves the parallelism with a timing test, dispatches to *different* worker nodes, covers the empty fan-out trap, and ends with a full LLM-planned map-reduce where the model decides the branch count.

**05 — Composed pipeline.** A content pipeline whose parent has four boxes and six state keys. Behind them: a research subgraph that internally fans out with `Send`, and a write-and-grade subgraph that internally loops on a failing grade up to a capped number of attempts. Both attached with adapter functions, so the parent's vocabulary never touches the children's. Shows that no child private key reaches the parent, streams each layer, checkpoints the composed graph, and lists what would change for production.

## How to run

1. Put a Groq key in `03_agentic_ai/.env`:
   ```
   GROQ_API_KEY=gsk_...
   ```
   Every notebook walks up the directory tree to find that file, so it works from any working directory.
2. Open the notebooks in order (01 → 05) and run all cells.

**Models.** Groq (`qwen/qwen3.8-27b`) is primary; a local Ollama server (`llama3.1:8b` at `localhost:11434`) is the fallback if no key is present. OpenAI is never used.

**Rate limits.** Groq's free tier is roughly 8000 tokens per minute. Every notebook uses a `safe_invoke` helper that paces calls and backs off exponentially on HTTP 429. Notebook 05 makes the most calls (roughly a dozen); if you hit a limit, wait a minute and re-run the cell.

## Prerequisites

- [01_graph_basics](../01_graph_basics/README.md) — `StateGraph`, nodes, edges, conditional routing, and especially **state reducers**, which notebook 04 depends on
- [02_tool_using_agents](../02_tool_using_agents/README.md) — agents as graphs
- [03_persistence_checkpointing](../03_persistence_checkpointing/README.md) — checkpoint namespaces in notebooks 01, 02 and 05 build on this
- [05_streaming](../05_streaming/README.md) — `stream_mode="updates"`, extended here with `subgraphs=True`
- [06_multi_agent_systems](../06_multi_agent_systems/README.md) — `04_parallel_agents` mentions `Send` in passing; notebook 04 here is the full treatment

## What you'll learn

- Why a flat graph stops scaling, in four concrete and reproducible failure modes
- How to compile a graph and use it as a node in another graph
- The difference between shared-schema embedding and isolated-schema wrappers, and how to choose
- Why mismatched output key names lose data **silently**, and how to catch it in one line
- How `Send` creates branches at runtime, why the worker needs its own schema, and why the collector key needs a reducer
- How to layer isolated subgraphs, `Send` fan-out and retry loops into one maintainable system

## Next

**[08_advanced_reasoning_patterns](../08_advanced_reasoning_patterns/README.md)** — using composition to build alternatives to the ReAct loop: Reflexion, Plan-and-Execute, and ReWOO.
