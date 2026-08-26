# LCEL and Runnables [Step 4 - Composable chains]

> **MLCourse - Agentic AI - LCEL and Runnables**

> Stage in the capstone: the entire RAG pipeline IS one runnable chain; memory wrapping uses RunnableWithMessageHistory.

LangChain Expression Language (LCEL) is not a new language - it is one insight: every
piece of an LLM application can expose the same tiny interface, and then composition
becomes operator overloading. Templates, models, parsers, retrievers, even your own
functions all implement the `Runnable` protocol, so they snap together with `|` like
LEGO studs. Master the protocol and RAG, agents, and memory all read as variations of
one shape.

## What you'll learn

- the mental model: everything is a `Runnable` speaking `invoke` / `batch` / `stream`
- how `|` builds sequential pipelines and dicts of runnables build parallel fan-outs
- the component catalog - from `ChatPromptTemplate` to `RunnableParallel` - and the job of each
- how to add resilience (`with_fallbacks`) and pin settings (`bind(stop=...)`)
- which half of a chain you can develop and test completely offline

## 1. Mental model: everything is a Runnable

Any component worth its place implements exactly three verbs:

- `invoke(input)` - one input in, one output out. The primitive everything reduces to.
- `batch([a, b, c])` - many inputs in, outputs out as a list, order preserved.
- `stream(input)` - a lazy iterator yielding intermediate chunks as stages finish.

Uniformity is the whole trick. Because a prompt, a chat model, a parser, and your own
Python function all answer to the same three calls, you can: swap any stage without
touching neighbors (mock the model offline, go live by changing one variable),
orchestrate generically (retry, fallback, batch - the framework does not know or care
what a stage does internally), and reason locally (each stage is a type adapter:
dict-to-messages, messages-to-reply, reply-to-string).

## 2. Composition grammar

Five rules cover essentially every LCEL program you will write:

- `a | b` - sequential: b receives whatever a produces. Build long chains incrementally
  and inspect each prefix with `.invoke()` before appending the next stage.
- `{"k1": r1, "k2": r2}` piped after an input (or `RunnableParallel(k1=r1, k2=r2)`) -
  fan-out: both branches consume the SAME input concurrently; results merge into a dict.
- `RunnablePassthrough().assign(new_key=fn)` - keep the incoming dict intact and ADD
  computed keys. This is how retrieval slots context next to the untouched question.
- `.with_fallbacks([backup])` - try the wrapped runnable; on failure, transparently
  try the backups in order.
- `.bind(stop=[...])` or other kwargs - pin generation settings onto an existing
  runnable without rewriting the chain.

## 3. Component catalog

| Component | Import from | Job in the chain |
|---|---|---|
| `ChatPromptTemplate` | `langchain_core.prompts` | dicts in, rendered messages out |
| Chat model (e.g. `ChatGroq`) | provider package | messages in, `AIMessage` out |
| `StrOutputParser` | `langchain_core.output_parsers` | `AIMessage` in, plain `str` out |
| `CommaSeparatedListOutputParser` | `langchain_core.output_parsers` | text in, `list[str]` out |
| `PydanticOutputParser` | `langchain_core.output_parsers` | text in, validated model instance out |
| `RunnableLambda` | `langchain_core.runnables` | wraps ANY Python function as a chain stage |
| `RunnablePassthrough` | `langchain_core.runnables` | identity stage; `.assign()` extends its output dict |
| `RunnableParallel` | `langchain_core.runnables` | fans one input out to branches, merges results |
| `RunnableWithMessageHistory` | `langchain_core.runnables` | wraps a chain with automatic per-session history |
| `.with_fallbacks([...])` | method on any Runnable | resilience: backup stages on failure |
| `.bind(**kwargs)` | method on any Runnable | freeze extra kwargs (e.g. `stop=["Observation"]`) |

## 4. When and how

- Prototype offline FIRST: `RunnableLambda` stages cost nothing, need no keys, and
  fail fast. Swap in the live model as the last step - the chain shape never changes.
- Inspect prefixes: `prompt_only.invoke({...}).to_string()` shows exactly what the
  model will see; debug chains one stage at a time, never whole.
- Expect stream granularity honestly: a chain streams chunk-by-chunk only while every
  stage supports it; a buffering stage (most parsers) collapses the stream to one
  chunk per upstream emission. Token-smooth UX usually means `prompt | model` streamed,
  parser applied afterwards.
- Batch for throughput: `.batch()` reuses one composed chain across inputs; output
  order always matches input order, so zip results back onto requests safely.

> **Common pitfall:** pipe order is type flow. `(prompt | parser)` feeds the parser a
> prompt-value instead of a model reply and explodes with a confusing traceback. Read
> chains aloud left to right - "prompt, then model, then parser" - and keep each
> stage's input type equal to its neighbor's output type.

> **Pro tip:** `.assign(fn)` hands your function the ENTIRE dict accumulated so far,
> not just one key. Return values land under the new key; same-name keys overwrite
> inputs, so treat `.assign` as "derive and append", never "mutate".

## 5. Contents

1. `02_runnables_deepdive.nb.py` - the protocol made tangible: uniform
   `invoke`/`batch`/`stream` across lambdas and prompts, `prompt | model | parser`
   assembled stage by stage (live model swaps for an offline echo when no key exists),
   `RunnableLambda` glue, the passthrough-plus-assign mini RAG shape, a
   summary-plus-keywords `RunnableParallel` fan-out, guarded `with_fallbacks`,
   token-by-token `.stream()`, `.batch()`, and a `bind(stop=...)` truncation demo -
   roughly half the notebook runs with zero providers.
2. `01_output_parsers_str_list.nb.py` - gentlest possible chains: `StrOutputParser`
   and `CommaSeparatedListOutputParser` piped at the END of `prompt | llm`, format
   instructions shown verbatim and embedded correctly, with offline twins of every
   parsing step and a bridge forward to the Pydantic tier.

## Summary

- One protocol (`invoke`/`batch`/`stream`), one operator (`|`), two combinators
  (parallel dicts, `.assign`) - that is LCEL.
- Chains are data: build incrementally, inspect prefixes, mock stages offline, swap
  providers without redesign.
- Parsers are just terminal runnables; resilience and settings are decorators on any
  runnable (`with_fallbacks`, `bind`).
- In the capstone this pays off completely: retrieve, format, answer, and cite are
  one runnable chain, wrapped with `RunnableWithMessageHistory` so multi-turn chat
  remembers without leaking into your core logic.
