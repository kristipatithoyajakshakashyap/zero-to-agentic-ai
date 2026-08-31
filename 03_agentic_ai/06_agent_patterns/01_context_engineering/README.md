# Module 01: Context Engineering

> **MLCourse - Agentic AI - Agent Patterns**

Everything an LLM knows on a given turn is whatever you put in one flat string. This module is about deciding, measuring and enforcing what goes into that string.

## The concept

There is no session, no memory and no state inside a chat model. Every call is stateless, and every call is assembled from the same five components:

```
        +---------------------------------------------------------+
        |                   THE CONTEXT WINDOW                    |
        +---------------------------------------------------------+
        | 1. SYSTEM PROMPT      role, rules, output format        |
        | 2. TOOL SCHEMAS       every tool's name/description/args|
        | 3. RETRIEVED DOCS     whatever RAG pulled in            |
        | 4. CONVERSATION       every prior user+assistant turn   |
        | 5. THE USER'S QUERY   usually the smallest piece        |
        +---------------------------------------------------------+
```

Prompt engineering is about the wording of component 1. **Context engineering is about the allocation across all five** — which is where almost all of the cost, latency and accuracy of a real agent actually lives.

## Why it matters

Three failures that look like different bugs are all the same bug:

- **"It got expensive."** History is resent every turn, so per-call cost grows linearly and cumulative cost grows quadratically. In notebook 01 a ten-turn session is measured at 9,685 tokens for what feels like ten short questions.
- **"It forgot my constraint."** Recency trimming — the default in every framework — drops the oldest turns first, and the user's hard constraint was usually stated early.
- **"It ignored the document I gave it."** Being inside the window is not the same as being read. Position affects accuracy, and reordering costs nothing.

None of these are fixed by a better prompt or a bigger model. They are fixed by measuring the window and budgeting it.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_what_goes_in_the_window](01_what_goes_in_the_window.ipynb) | The five components, measured; local estimate vs. the provider's billed count |
| 02 | [02_token_budget](02_token_budget.ipynb) | A budget as data, with an enforcer; the real A/B-measured cost of tool schemas |
| 03 | [03_trimming_strategies](03_trimming_strategies.ipynb) | Recency vs. relevance vs. priority on one over-budget conversation, plus the hybrid |
| 04 | [04_lost_in_the_middle](04_lost_in_the_middle.ipynb) | A real positional experiment: needle at five positions, three trials each |
| 05 | [05_structured_vs_prose](05_structured_vs_prose.ipynb) | The same facts as prose, JSON, key/value and a table — tokens *and* accuracy |

### Walkthrough

**01 — What goes in the window.** Assembles a realistic support-agent request by hand and prints a per-component token table. The headline result is that the user's actual question is ~4% of the request while the tool schemas are ~38%. It then sends the request for real and reconciles the local `cl100k_base` estimate against the provider's `usage_metadata` (measured: +12.8%, a systematic gap from the chat template, not noise). Closes by projecting history growth over ten turns — linear per call, quadratic cumulatively.

**02 — The token budget.** Turns those measurements into a ceiling plus named allocations that sum to it, including the allocation everyone forgets: **reserved output**. The tool-schema cost is then measured properly by sending one question twice, with and without tools bound, and reading `input_tokens` off both responses. Ends with the four moves available when a component overflows — drop, compress, reallocate, raise the ceiling — and a prominent warning about truncating mid-item instead of dropping whole units.

**03 — Trimming strategies.** A trip-planning conversation with a landmine: a severe peanut allergy stated at turn 2, then buried under fourteen turns of chit-chat, then a food question. Recency, relevance (local `fastembed` embeddings, no network round-trip) and priority-tiering all get the same 160-token budget, and the notebook reports for each whether the constraint survived *and* whether the reply showed awareness of it — deliberately as two separate columns, because a safe-sounding answer is not evidence the model knew. Ends with the hybrid you should actually ship: pinned, then recent, then relevant.

**04 — Lost in the middle.** The experiment done properly: one needle, sixteen confusable distractors of identical shape, invented facts so pretraining cannot help, and only the position varying. Five positions x three trials, then a harder variant with a near-duplicate look-alike record to raise difficulty without raising token count. The notebook is explicit that a flat 100% result is a *legitimate* finding at this context size and says so in the output rather than pretending an effect appeared. Closes with the three cheap consequences: rerank, sandwich the instruction, retrieve less.

**05 — Structured vs. prose.** Five order records rendered five ways, measured for tokens and then for comprehension on five lookup questions. The rule that falls out is not "models like JSON" — it is that **repeated field names are the tax**, so a Markdown table beats per-row JSON, and `json.dumps(indent=2)` is the most expensive option available. Then the counter-case: a causal question ("should we refund Jonas?") that the table structurally cannot answer and one sentence of prose can.

## How to run

From the repo root, with the project virtualenv:

```bash
.venv/Scripts/python -m jupyter lab      # then open the notebooks in order
```

Or execute a notebook headlessly with `nbclient` (the `jupyter nbconvert` CLI is broken in this environment):

```python
import nbformat
from nbclient import NotebookClient

nb = nbformat.read("01_what_goes_in_the_window.ipynb", as_version=4)
NotebookClient(nb, kernel_name="python3",
               resources={"metadata": {"path": "."}}).execute()
nbformat.write(nb, "01_what_goes_in_the_window.ipynb")
```

The notebooks are independent — you can run any one of them on its own — but they are written to be read in order.

### Model and keys

All notebooks use **Groq** (`qwen/qwen3.8-27b`) via `ChatGroq`. `GROQ_API_KEY` is read from `03_agentic_ai/.env`, which every notebook locates with the same walk-up block. A local Ollama model would work as a drop-in alternative; OpenAI is never used anywhere in this course.

The Groq free tier allows 8,000 tokens per minute. The shared `chat()` helper in each notebook self-paces to stay under that ceiling and retries with exponential backoff on a 429, so the multi-call experiments in notebooks 03-05 run unattended.

### Extra dependencies

Notebook 03 uses `fastembed` (ONNX, CPU, no GPU and no torch) for local relevance scoring. Everything else is `langchain-groq`, `tiktoken` and `python-dotenv`.

## Prerequisites

| Module | Why |
|---|---|
| [01_langchain/01_fundamentals](../../01_langchain/01_fundamentals) | Chat models, message roles, `usage_metadata` |
| [01_langchain/04_tools_and_agents](../../01_langchain/04_tools_and_agents) | Where tool schemas come from and what binding them does |
| [03_rag_advanced/11_reranking](../../03_rag_advanced/11_reranking) | Relevance scoring; notebook 04 explains *why* reranking helps |
| [02_langgraph/03_persistence_and_memory](../../02_langgraph/03_persistence_and_memory) | Conversation state — the component that grows |

## Recap

| Idea | Takeaway |
|---|---|
| Five components | Measure each one; the query is almost never the expensive part |
| Estimate vs. billed | Local tokenizers are approximate — reconcile once, then correct |
| Budget as data | A ceiling, named allocations, an enforcer, and reserved output |
| Drop whole units | Never slice a document or a conversation turn in half |
| Pin constraints | Recency loses old constraints; relevance loses off-topic ones |
| Position matters | In the window is not the same as read — rerank, sandwich, retrieve less |
| Format for cost | Name columns once; indented JSON is billable whitespace |

**Next module:** [02_memory_at_scale](../02_memory_at_scale) — what to do when the conversation outgrows every budget you can set.
