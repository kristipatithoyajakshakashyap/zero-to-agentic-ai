# Module 02: Memory at Scale

> **MLCourse - Agentic AI - Agent Patterns**

The memory modules earlier in this course (`02_langgraph/03_persistence_and_memory`, `04_crewai/02_advanced_agents/03_memory_systems`) store the full message history and replay it. That is correct, and it works beautifully — until the conversation is long enough that replaying it is slow, expensive, or simply rejected. This module starts exactly where those modules stop working.

## The concept

An unbounded conversation fails in three distinct ways, in this order:

```
  1. COST      grows quadratically with turn count, silently
  2. ATTENTION the model reads the middle of a long thread worse than the ends
  3. HARD LIMIT the API eventually rejects the request outright
```

Most systems only plan for #3, because it is the only one that raises an exception. #1 and #2 are the ones that actually cost you, and they never announce themselves.

The fix is not a bigger window. It is a **working set** — a bounded amount of context, rebuilt each turn from a bounded summary of the past plus a small buffer of the present — combined with a written **retention policy** that says which facts are never allowed to be lost regardless of how the working set is built.

## Why it matters

Notebook 01 measures the naive fix — keep the last *k* turns — against a full transcript on a conversation with a hard constraint (EU-only hosting) stated in turn 5 and needed again in turn 30. Truncation saves most of the tokens and silently drops every constraint stated in the first half of the conversation, because constraints are almost always stated early and recency filters are biased against exactly that. Nothing in your logs tells you this happened; a user finds out for you.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_when_the_window_overflows](01_when_the_window_overflows.ipynb) | The three failures, measured; a reusable recall grader; why truncation is a filter on time, not importance |
| 02 | [02_rolling_summarization](02_rolling_summarization.ipynb) | Summary + verbatim buffer, rewritten (not appended) on overflow; compounding drift, named and measured |
| 03 | [03_hierarchical_summaries](03_hierarchical_summaries.ipynb) | A gist / chapter / raw-turn tree, built bottom-up, with drill-down retrieval for detail questions |
| 04 | [04_preserve_vs_discard](04_preserve_vs_discard.ipynb) | A four-category retention policy and an append-only fact store immune to drift by construction |
| 05 | [05_mem0_local](05_mem0_local.ipynb) | The same ideas, productised — `mem0` running fully locally: Groq LLM, `fastembed` embedder, FAISS store |

### Walkthrough

**01 — When the window overflows.** Measures cumulative token cost across a 30-turn conversation (quadratic, as expected), then compares full-transcript memory against "keep the last 8 turns" using a set of probe questions graded automatically. Every durable fact in the test conversation — the product name, the budget, the pilot customer — was stated in the first half; truncation loses essentially all of them. Introduces the vocabulary the rest of the module uses: working set, compression, retention.

**02 — Rolling summarization.** The standard fix, built from scratch: a verbatim buffer plus a summary that is **rewritten**, never appended to, each time the buffer overflows. Demonstrates the failure nobody warns you about — compounding drift, where an error introduced at fold 1 is baked into every later summary because nothing re-reads the original turns — and names four mitigations. Measures the working-set size curve (bounded, not shrinking) against recall (usually well above truncation, below the full transcript).

**03 — Hierarchical summaries.** Instead of one flat summary, a tree: raw turns on disk, chapter summaries, a merged mid-level, and a whole-thread gist that is always resident. The payoff is **drill-down** — routing a detail question to the one relevant chapter via a local embedding lookup, then answering from its raw turns, at a fraction of the tokens a full-transcript answer would cost. Explicit about the trade: hierarchy buys optional depth, not necessarily higher baseline recall than a good rolling summary.

**04 — Preserve vs. discard.** The policy question underneath every mechanism: a four-category taxonomy (constraint, decision, context, chatter) with a different rule for each, and an **append-only fact store** that pins constraints and decisions outside the summariser entirely — immune to the drift from notebook 02 by construction, because nothing ever rewrites it. Measures recall of a lossy summary alone, the fact store alone, and both together, and shows exactly which durable facts each one keeps.

**05 — mem0 in local mode.** The same mechanism as notebook 04, as a real library: `mem0.Memory` configured with `llm: groq`, `embedder: fastembed`, `vector_store: faiss` — everything runs on the local machine except the Groq LLM call. Covers `add` (with `infer=False`, and why — mem0's default extraction prompt is too large for the Groq free tier's 8000 TPM ceiling), `search` with a required score threshold, `get_all`, and `delete`-based supersession. Closes with a table of what mem0 handles (storage, embedding, scoping) versus what remains yours (what counts as durable, the threshold, the retention policy) — which is the entire content of notebook 04.

## How to run

```bash
.venv/Scripts/python -m jupyter lab
```

or headlessly with `nbclient` (the `jupyter nbconvert` CLI is broken in this environment):

```python
import nbformat
from nbclient import NotebookClient

nb = nbformat.read("01_when_the_window_overflows.ipynb", as_version=4)
NotebookClient(nb, kernel_name="python3",
               resources={"metadata": {"path": "."}}).execute()
nbformat.write(nb, "01_when_the_window_overflows.ipynb")
```

Every notebook imports the shared conversation from **`conversation_data.py`**, which lives in this folder — a 30-turn product-planning thread with a labelled set of durable facts and probe questions used to grade recall consistently across all five notebooks. Read it once before the notebooks; nothing in the notebooks pastes the conversation inline.

### Model and keys

All notebooks use **Groq** (`qwen/qwen3.8-27b`) via `ChatGroq`, with `GROQ_API_KEY` read from `03_agentic_ai/.env`. OpenAI is never used. The shared `chat()` helper self-paces under the Groq free tier's 8,000-token-per-minute ceiling and retries with backoff on a 429 — several notebooks make 15-40 calls (summarisation folds, per-chapter builds, probe grading), so this matters more here than in module 01.

### Extra dependencies

- `fastembed` — local ONNX embeddings for relevance scoring (notebook 03) and mem0's embedder (notebook 05). No GPU, no torch.
- `mem0` — notebook 05 only, configured for `faiss` + `fastembed`, never the hosted platform. `ANONYMIZED_TELEMETRY=False` is set before any chromadb/mem0 import.

Notebook 05 writes a local store to `.mem0_store/` inside this folder; it is gitignored and rebuilt fresh on every run.

## Prerequisites

| Module | Why |
|---|---|
| [01_context_engineering](../01_context_engineering) | The budget this module's working set has to fit inside |
| [02_langgraph/03_persistence_and_memory](../../../02_langgraph/03_persistence_and_memory) | Full-history memory — the thing that breaks here |
| [04_crewai/02_advanced_agents/03_memory_systems](../../../04_crewai/02_advanced_agents/03_memory_systems) | The framework-level memory API this module explains the internals of |
| [03_rag_advanced](../../../03_rag_advanced) | Vector search and retrieval, used for relevance scoring and drill-down |

## Recap

| Idea | Takeaway |
|---|---|
| Three failures | Cost, attention, hard limit — cost bites first and is silent |
| Truncation is deletion | Cheap, and biased against early-stated constraints |
| Rewrite, never append | The only rolling-summary design that stays bounded |
| Compounding drift | Errors at fold 1 are permanent — name the must-keep categories |
| Hierarchy buys drill-down | Gist resident, detail retrievable on demand |
| Constraints are cheap to keep | Pin them outside the summariser; supersede, never delete |
| A library is the mechanism, not the policy | mem0 handles storage; you still decide what is durable |

**Next module:** [03_sampling_and_search](../03_sampling_and_search) — spending *more* calls, deliberately, to buy accuracy, and measuring whether it worked.
