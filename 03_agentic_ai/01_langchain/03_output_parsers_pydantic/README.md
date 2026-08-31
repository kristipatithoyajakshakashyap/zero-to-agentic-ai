# Output Parsers and Pydantic Schemas [Step 3 - Structured LLM output]

> **MLCourse - Agentic AI - Output Parsers and Pydantic**

> Stage in the capstone: capstone answers are parsed into a strict AnswerWithSources schema so citations cannot hallucinate.

A chat model is a text function: bytes go in, most-likely tokens come out. Useful
software, however, needs *values* - a float it can threshold, a list it can render,
an object it can store. This module is the bridge between those two worlds: parsers
turn model prose into Python data, and pydantic guarantees the data deserves the
name of its type.

## What you'll learn

- why unstructured LLM text breaks downstream software, quietly and late
- the four parser tiers - string, comma-separated list, JSON, Pydantic - and when each earns its place
- how pydantic v2 validates fields, nests models, enforces custom rules, and round-trips JSON
- two ways to force a real model into the `AnswerWithSources` contract: native `with_structured_output` and prompt-based `PydanticOutputParser`

## 1. Why unstructured LLM text breaks software

Ask a model for "the answer, the sources, and a confidence score" and you receive a
friendly paragraph. Extracting values from that paragraph with string surgery looks
harmless until it is not:

```python
text = llm.invoke(question).content                 # a str, every time
confidence = float(text.split("Confidence:")[1][:4])  # IndexError roulette
sources = text.split("Sources:")[1].splitlines()      # hope the model kept the layout
```

Three failure modes follow, and they compound:

- **Late crashes**: the split succeeds today, dies next Tuesday when the model phrases
  the section differently. The explosion lands far from the cause.
- **Silent corruption**: `"confidnce: 0.9"` parses as garbage nobody notices until a
  chart looks wrong or a database rejects a write.
- **Untestable pipelines**: prose has no shape, so unit tests degenerate into
  eyeballing printouts.

A parser plus a schema moves the failure to the boundary, makes it loud, and makes it
specific: one exception naming the exact field that violated the exact constraint.

## 2. The parser landscape

LangChain ships parsers in increasing levels of strictness. All of them are
`Runnable`s, so they pipe naturally at the END of a `prompt | llm` chain.

| Tier | Tool | Import | Returns | Reach for it when |
|---|---|---|---|---|
| string | `StrOutputParser` | `langchain_core.output_parsers` | `str` | you just want the message text, metadata stripped |
| list | `CommaSeparatedListOutputParser` | `langchain_core.output_parsers` | `list[str]` | quick enumerations: keywords, names, tags |
| JSON | `JsonOutputParser` | `langchain_core.output_parsers` | `dict` / `list` | flexible structure, no fixed contract yet |
| Pydantic | `PydanticOutputParser` | `langchain_core.output_parsers` | your `BaseModel` subclass | anything touching storage, UI, or business rules |

The modern shortcut sits above the table: `llm.with_structured_output(YourModel)`
negotiates a JSON / tool-calling mode with the provider and returns validated model
instances directly - no manual prompt clause, no text scraping. Prefer it whenever the
backend supports it; the `PydanticOutputParser` route remains the portable fallback
and the best teacher of what is actually happening. Both routes run side by side in
notebook 02 below.

## 3. When and how

Choosing a tier is choosing how much you promise the rest of your program:

- Prose for humans (summaries, replies)? `StrOutputParser` and done.
- A bag of items you will iterate? Comma-separated list - cheap, readable, weakly typed.
- Shape varies per request? `JsonOutputParser` gives dicts, but YOU validate semantics.
- Fields feed filters, thresholds, database columns, or agents? Pydantic, always.

How to wire whichever you picked:

- Pipe the parser **last**: `chain = prompt | llm | parser`. Left-to-right, each stage
  consumes the previous stage's output type; the parser converts the final
  `AIMessage` into real data.
- Prompt-driven parsers must TEACH the format: embed
  `parser.get_format_instructions()` into the prompt via `.partial(format_instructions=...)`.
  The parser validates; it never instructs.
- Catch the specific alarms: `ValidationError` (pydantic) for contract violations you
  caused, `OutputParserException` for model output that drifted off-contract.

> **Common pitfall:** loose schemas - declaring every field as `str` "to be safe".
> You gain crash-freedom and lose every guarantee: `confidence="high"` sails through
> and detonates later. Constrain early (`ge`, `le`, `max_length`), narrow types, and
> let validation earn its keep.

> **Pro tip:** write the pydantic model BEFORE the prompt. Its field names and
> descriptions get shipped to the model as part of format instructions, so schema
> design is prompt engineering. Vague descriptions produce vague fills.

## 4. Contents

Work through them in file order:

1. [01_pydantic_concepts.ipynb](01_pydantic_concepts.ipynb) - pure pydantic fundamentals, no LLM anywhere: typed
   fields with `Field` constraints, `ValidationError` dissected via `.errors()`,
   nested `Address` inside `Customer`, `@field_validator` normalization rules, and
   lossless dict/JSON round trips - the contract skills every later module assumes.
2. [02_pydantic_with_llms.ipynb](02_pydantic_with_llms.ipynb) - the payoff notebook: define `AnswerWithSources`,
   then fill it three ways - guarded `ChatGroq` via `with_structured_output`
   (Route A), the `PydanticOutputParser` fallback with format instructions printed
   verbatim and `OutputParserException` handled (Route B), and a hand-written JSON
   replay that teaches offline with zero API keys (Route C).

Hands-on wiring of the string and list parsers into chains lands in module 04
(LCEL), where parsers become ordinary pipe segments.

## Summary

- Model output is prose; software needs values - parse at the boundary or fail late.
- Four tiers, one rule: pick the strictest tier your use case can justify.
- `with_structured_output` first, prompt-and-parse as the portable fallback.
- Format instructions belong IN the prompt; exceptions belong in YOUR handler.
- In the capstone this discipline is non-negotiable: answers must satisfy
  `AnswerWithSources` or they never reach the user - citations cannot hallucinate
  through a validated schema.
