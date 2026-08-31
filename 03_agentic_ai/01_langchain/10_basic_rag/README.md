# Step 10 - Basic RAG (Retrieval-Augmented Generation)

> **MLCourse - Agentic AI - Basic RAG**

> Stage in the capstone: THIS IS the generation core the capstone wraps memory around.

RAG in one sentence: instead of asking a model to remember your documents, you
**retrieve** the few chunks that likely contain the answer and let the model
answer **from YOUR documents, citing them** - retrieval finds the evidence, generation reads it out.

## Why RAG beats fine-tuning for knowledge problems

Fine-tuning teaches a model *behavior*; it is a poor database. When the goal is
"answer questions about THIS book/manual/wiki", RAG wins on three axes:

| Axis | Fine-tuning | Basic RAG |
|---|---|---|
| Cost | GPU hours every time knowledge changes; retrain to add one paragraph | Re-embed only changed chunks; seconds of CPU |
| Freshness | Frozen at training time - new facts need a new run | Swap or append files and the index updates immediately |
| Citations | The model cannot point at where it "knows" something | Every answer can name chunk `[12]`, so humans can verify |

Rule of thumb: fine-tune for style/format/behavior ("always answer as a pirate"),
use RAG for facts that live in your corpus. This track is 100 percent RAG.

## The six-step pipeline

Every RAG application on earth is this diagram; each step maps to one module you
have already met:

```
INGEST          CHUNK           EMBED           STORE           RETRIEVE        GENERATE
module 05   ->  module 06   ->  module 07   ->  module 08   ->  module 09   ->  modules 02+03+04 + this module
loaders         strategies      embeddings      chroma/faiss    retrievers      prompts+pydantic+LCEL
alice.txt       recursive       MiniLM 384-d    persist disk    top-k / MMR     answer ONLY from context
                500/100                                                         cite [id] tags
```

The capstone adds exactly one box after GENERATE: **memory** (Step 11).

## Anatomy of the minimal chain

The whole notebook builds this single expression, piece by piece:

```python
rag_chain = {"context": fetch_context, "question": itemgetter("question")} | prompt | llm | StrOutputParser()
```

- `{"context": ..., "question": ...}` - a dict of runnables becomes a parallel
  fan-out: both values receive the input `{"question": "..."}` at once.
  `fetch_context` calls the retriever and formats hits as `[id] text` blocks;
  `itemgetter("question")` copies the raw question through untouched.
- `prompt` - a `ChatPromptTemplate` whose system message forbids outside
  knowledge and demands `[id]` citations; its `{context}` slot receives the
  formatted chunks. The sibling idiom `RunnablePassthrough.assign(context=...)`
  does the same job while keeping existing keys - the notebook runs BOTH.
- `llm` - Ollama `llama3.2` locally (guarded), with a clearly-labelled offline
  stub fallback so the pipeline still executes on machines without models.
- `StrOutputParser` - unwraps the final `AIMessage` into a plain string.

Read it right-to-left when debugging: did parsing work? did generation follow the
rules? was the retrieved context even relevant? Most "bad RAG" failures are
retrieval failures wearing a generation costume.

## When to reach for RAG

- The knowledge lives in private or fast-changing documents.
- Users need verifiable answers with sources.
- The corpus is far larger than any context window.
- You want predictable cost: retrieve 4 chunks, not 200 pages.

## How to know it works (the cheap evaluation)

- Grounding check: do the cited `[id]`s actually appear among the chunks you
  retrieved? (The notebook checks this automatically per question.)
- Refusal check: an out-of-corpus question should produce
  "I cannot find that in the provided excerpts", not a confident guess.
- Eyeball pass: print the retrieved chunk previews next to each answer and grade
  relevance by hand - unglamorous, and how most real teams still start.

## Common pitfalls

- **Context overflow**: stuffing the whole book into the prompt blows the context
  window and dilutes attention - chunk small and retrieve few (`k = 3..5`).
- **Wrong k**: too few chunks miss the evidence; too many bury it under noise and
  cost tokens. Tune k against real questions, not vibes.
- **Uncalibrated confidence**: LLMs sound equally sure whether or not the context
  contains the answer. Force citations plus an explicit refusal line, then verify.
- **Duplicate indexing on rerun**: re-running `add_documents` doubles the index -
  open-and-reuse first, rebuild only when empty (the notebook's defensive pattern).
- **Stale index**: if the source file changes but the persisted store does not,
  answers silently rot. Version or timestamp your indexes.

## Contents

1. [01_minimal_rag_pipeline.ipynb](01_minimal_rag_pipeline.ipynb) - defensive corpus recreation, `[id]`-tagged
   formatting, dict-prelude AND assign idioms side by side, three real Alice
   questions with evidence previews, World-Cup refusal demo, Groq comparison
   behind a key guard, printed eyeball checklist.

After this module continue to `11_memory_and_state` to give this chain a memory.

## Summary

RAG = retrieve relevant chunks, paste them into a rule-bound prompt, generate a
cited answer. It beats fine-tuning for knowledge because it is cheap, fresh, and
verifiable. The six steps ingest-chunk-embed-store-retrieve-generate map one-to-one
onto modules 05-09 plus everything you know about prompts and LCEL. Master the
minimal chain here; the capstone merely wraps it in sessions, memory, and polish.
