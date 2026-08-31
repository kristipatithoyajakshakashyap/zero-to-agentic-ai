# Module 05: Semantic Routing

> **MLCourse - Agentic AI - Agent Patterns**

Decide **where a request should go before you spend anything on it**. An embedding
comparison against a few dozen example utterances costs microseconds and zero
tokens, and every request it diverts to a canned answer, a database lookup or a
line of Python is a model call you never pay for.

## What the concept is

A **route** is three things: a name, a handful of example utterances, and a handler.
There is no training step and no classifier to fit.

```
user request
     |
     v
 [ EMBED ]  ~5 ms CPU, 0 tokens
     |
     v
 cosine similarity against every route's example vectors (precomputed at startup)
     |
     +-- score >= threshold --> that route's handler   (canned text / SQL / Python)
     |
     +-- score <  threshold --> FALLBACK: the full model
```

The router is not a model call. That is the entire point: if you spend an LLM call
deciding which LLM call to make, you have doubled your call count to save at most
one. Notebook 01 measures exactly that.

## Why it matters

- It is the cheapest cost lever in an agent stack, and it is orthogonal to the
  others (caching, smaller models, shorter prompts) - they compose.
- It gives you **consistent, approved answers** on your most common questions,
  instead of a fresh paraphrase every time.
- It is measurable end to end: coverage, tokens, dollars, latency, and the error
  rate it introduces. Notebook 04 reports all five.
- The same "cheap stage in front of an expensive stage" shape appears in reranking,
  guardrails and tool selection. Learning it here transfers.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_route](01_why_route.ipynb) | Embedding router vs LLM router, measured; topic-vs-intent failure |
| 02 | [02_building_a_route_set](02_building_a_route_set.ipynb) | Max vs centroid, margins, the separation matrix, rules + embeddings |
| 03 | [03_thresholds_and_fallback](03_thresholds_and_fallback.ipynb) | Score distributions, the threshold sweep, the fallback route |
| 04 | [04_measuring_the_saving](04_measuring_the_saving.ipynb) | A 24-request workload, always-model vs routed, honest ledger |

### Walkthrough

**01 - Why route at all.** Builds a four-route set and the max-similarity router in
about fifteen lines, then races it against the obvious alternative - asking the model
to classify. On this run the embedding router was **17x faster and cost $0** against
**$0.000103 for six LLM classifications** ($17.09 per million requests for the router
*alone*). Closes on the failure mode that matters: embeddings match **topic**, not
**intent**, so "where is order 1042" and "I want to cancel order 1042" land on the
same route with similar confidence.

**02 - Building a route set.** The work you actually spend time on. Compares `max`
against `centroid` scoring on a held-out set written before any tuning (**0.938 vs
0.875** here). Introduces **margin** - top score minus runner-up - as the diagnostic
that predicts incidents better than accuracy does, and a **separation matrix** over
the routes themselves; the closest pair was `shipping_faq` <-> `order_status` at
**0.432**, which is exactly the pair a topic-based router cannot separate. Fixes it
with a high-precision regex rule *in front of* the embeddings. Ends by testing the
"just add more examples" instinct: adding a paraphrase and adding genuinely new
phrasing both left accuracy at **0.938 - no change** - and says plainly that a
16-utterance evaluation cannot detect small effects.

**03 - Thresholds and the fallback route.** Measures the in-domain and
out-of-domain score distributions (they overlap - out-of-domain text does not score
near zero), then sweeps the threshold and prints coverage, routed accuracy and
misroute rate at each step. Then the key move: the two error types are **not the
same size of mistake**, so plain accuracy optimises the wrong thing. A 5x misroute
penalty picks the threshold instead. Builds the full router with a real fallback that
logs *why* it was reached - `low confidence` (a route you have not written yet) vs
`handler declined` (right route, missing information).

**Measured threshold sweep** (16 in-domain + 8 out-of-domain utterances):

| threshold | coverage | routed acc | misroute rate | weighted loss |
|---|---|---|---|---|
| 0.20 | 0.750 | 0.889 | 0.250 | 10.0 |
| **0.25** | **0.667** | **1.000** | **0.000** | **0.0** |
| 0.45 | 0.625 | 1.000 | 0.000 | 1.0 |
| 0.60 | 0.333 | 1.000 | 0.000 | 8.0 |

**04 - Measuring the saving.** Runs a 24-request support workload (75% routable)
twice - once always calling the model, once through the router - and compares them
on identical instrumentation.

**Measured result:**

| | always-model | routed | saving |
|---|---|---|---|
| model calls | 24 | 5 | **79.2%** |
| total tokens | 1940 | 430 | **77.8%** |
| cost (USD) | 0.000755 | 0.000170 | **77.5%** |
| API seconds | 8.65 | 1.65 | **80.9%** |
| misroutes | n/a | **1** | - |

Per million requests of this mix: **$31.47 -> $7.07, saving $24.40.**

The one misroute is reported, not hidden: *"my parcel arrived with a missing item,
what now"* scored 0.576 on `shipping_faq` and got the stored delivery-times answer.
The notebook then states the three caveats that belong in any write-up of a number
like this - the saving is a property of the **traffic mix**, the routed answers are
**not the same answers**, and 24 requests cannot measure an error rate below ~4%.

## How to run

```bash
# from the repo root
.venv/Scripts/python -m jupyter lab   # or open the notebooks in VS Code
```

Run the notebooks in order; each is self-contained and re-runnable. Notebooks 01,
03 and 04 make Groq calls (roughly 40 small calls in total across the module);
notebook 02 makes none.

**Requirements**

- `GROQ_API_KEY` in `03_agentic_ai/.env`. The setup cell walks *up* to the folder
  containing `03_agentic_ai` and loads `03_agentic_ai/.env` from there - a subtle
  bug worth knowing about, because `load_dotenv` on a missing path fails silently.
- `sentence-transformers` (the `all-MiniLM-L6-v2` encoder, ~90 MB, CPU only) and
  `langchain-groq`.
- Model: `qwen/qwen3.8-27b` on Groq. A local Ollama model works as a substitute if
  you swap the two lines in `make_llm`; there is deliberately no automatic fallback
  branch, because a notebook that silently changes model produces numbers you
  cannot trust.

Groq's free tier is 8000 TPM, so the notebooks pace their calls and back off on
429s. Do not run several modules of this track at once.

## Prerequisites

| You should have done | Why |
|---|---|
| [`03_rag_advanced/02_hybrid_search`](../../03_rag_advanced/02_hybrid_search) | Embeddings and cosine similarity; the router is that machinery pointed at intents instead of documents |
| [`03_rag_advanced/11_reranking`](../../03_rag_advanced/11_reranking) | The same "cheap stage first, expensive stage second" pattern, and the habit of measuring the lift |
| [`01_langchain/02_chat_models_and_prompts`](../../01_langchain/02_chat_models_and_prompts) | `ChatGroq`, messages, and reading `usage_metadata` |

## Where to go next

- [`06_multi_agent_debate`](../06_multi_agent_debate) - the opposite trade: spend
  *more* to try to be righter, and measure whether it worked.
- [`05_production_security/03_caching_strategies`](../../05_production_security/03_caching_strategies) -
  the other big cost lever. Route first, then cache what reaches the fallback.
- [`02_langgraph/06_multi_agent_systems`](../../02_langgraph/06_multi_agent_systems) -
  routing between *agents* rather than handlers, with a model doing the deciding.
