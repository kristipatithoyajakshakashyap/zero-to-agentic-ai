# Steps 12-13 - Capstone Project: Chat With Alice

> **MLCourse - Agentic AI - Capstone RAG Chatbot**

> Stage in the capstone: this IS the capstone - every module above feeds this build.

## Project brief

Build **Chat With Alice**: a command-line RAG chatbot that answers questions
about *Alice's Adventures in Wonderland* from the book itself, cites the chunk
ids it used, refuses out-of-corpus questions instead of hallucinating, and keeps
**separate persistent named sessions** (for example `reader-1`, `reader-2`) so
two readers never share a memory. One notebook builds it phase by phase; your
job is to run it, read it, and then make the defensible design choices YOURSELF
in the marked justification cells.

## Stage checklist - every earlier module maps to a build phase

| Build phase | Reuses | What carries over from that module |
|---|---|---|
| PHASE 1 - ingest | 05 document loaders | `TextLoader` on download-once `DATA / "alice.txt"` |
| PHASE 2 - chunk | 06 chunking strategies | `RecursiveCharacterTextSplitter(500, 100)` + a written JUSTIFICATION cell |
| PHASE 3 - embed | 07 embeddings | HuggingFace MiniLM choice cell + dimension sanity check |
| PHASE 4 - index | 08 vector stores | Chroma persisted at `DATA / "chroma_capstone"`, collection `alice_rag` |
| PHASE 5 - retrieve | 09 retrievers | MMR with `k=4, fetch_k=16` config cell + rationale |
| PHASE 6 - generate | 02 prompts, 03 pydantic, 04 LCEL | role-based prompt, `AnswerWithSources` structured output, pipe composition |
| PHASE 7 - remember | 11 memory and state | `RunnableWithMessageHistory` over named sessions |
| PHASES 8-9 | everything | scripted evaluation + written findings |

The justification cells are the actual exam: "why recursive 500/100", "why this
embedder", "why this store", "why MMR k=4/fetch_k=16". Write answers a teammate
could act on.

## Rubric - the capstone passes when

1. **Runs top to bottom**: green on a fresh machine - Ollama missing falls back
   to the labelled offline stub, no Groq key prints a skip message, unsupported
   structured output drops to the string-parser path. Degradation is graceful,
   never fatal.
2. **Retrieval demonstrably relevant**: each factual answer is accompanied by its
   retrieved chunk ids/previews and those chunks genuinely contain the evidence.
3. **History demonstrably remembered**: follow-up questions ("summarize what I
   asked so far") reference earlier turns, and session `reader-2` cannot see
   anything asked in `reader-1`.
4. **Findings written**: PHASE 9 records what worked, retrieval misses actually
   observed during the eval run, and ideas explicitly deferred - not vibes,
   observations.

## Extension ideas (pick one for your portfolio)

- Swap the embedder (`bge-small-en-v1.5` or similar) and measure recall change.
- Add a cross-encoder reranker between retrieve and generate.
- Hybrid search: BM25 keywords union dense vectors before the prompt.
- Summary memory for long sessions (the Step 11 pointer made real).
- Stream tokens to the console for perceived speed.
- A golden Q/A test set (20 questions) scored automatically per commit.
- Page/paragraph citations instead of raw chunk indexes.
- Persist sessions with `SQLChatMessageHistory` so chats survive restarts.

## Contents

1. [01_capstone_rag_chatbot.ipynb](01_capstone_rag_chatbot.ipynb) - the complete nine-phase build:
   ingest, chunking with justification, embedding, indexing, MMR retrieval,
   structured-output RAG chain with offline fallback ladder, session memory,
   six-question scripted evaluation across two readers, findings, and an
   optional interactive mode behind `INTERACTIVE = False`.

This closes the track: loaders became an index, prompts became a contract,
chains became an application, and state became memory. Ship it.
