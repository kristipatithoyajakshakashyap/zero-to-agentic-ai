# Step 11 - Memory and State

> **MLCourse - Agentic AI - Memory and State**

> Stage in the capstone: the capstone chatbot remembers prior turns PER SESSION thanks to this.

Chat models are stateless functions: every `invoke()` starts from a blank slate,
so "what is my name?" fails unless you re-send the earlier conversation yourself.
Memory is simply **the discipline of storing past turns and injecting them back
into each prompt**. This module turns that idea into working, per-session machinery.

## Why stateless models need external memory

- The model has no notion of "this user" or "earlier": context is 100 percent of
  what you put in the messages list.
- Follow-up questions ("and what about HER sister?") are unanswerable without the
  antecedent turns - real chatbots live on follow-ups.
- Multi-user apps need each conversation kept separate; a single global transcript
  would leak one user's details into another's answers.

## The session-id pattern

One id string per conversation is the entire design:

```python
config = {"configurable": {"session_id": "reader-1"}}   # caller tags every invoke
chatbot.invoke({"input": "hi"}, config=config)          # wrapper loads THAT history
```

A factory callable (`get_session_history(session_id)`) returns the stored message
list for that id - creating it on first sight. Same id in, same history back;
different ids can never see each other. The capstone uses ids like `reader-1`.

## Buffer vs window vs summary

| Strategy | Keeps | Cost per turn | Recall quality | Scope in this track |
|---|---|---|---|---|
| Buffer | every message ever sent | grows forever (tokens resent each turn) | perfect, until the window overflows | implemented |
| Window | only the last N messages | constant | forgets old facts BY DESIGN | implemented |
| Summary | rolling LLM digest of old turns + recent raw turns | small prompt + one extra LLM call | gist survives, details lost | pointer only |

Honest scope note: we implement buffer and window end to end; summary memory is
described here so you know it exists, not coded - it is an excellent self-study
extension (see Step 12 extension ideas).

## The role of RunnableWithMessageHistory

`RunnableWithMessageHistory` is plumbing so your chain stays pure:

1. You write a chain that expects `{"input": ...}` plus a `history` placeholder.
2. The wrapper intercepts each call, reads `session_id` from the config,
   asks the factory for that session's messages, injects them under
   `history_messages_key`, runs your chain, then appends the new human/AI pair
   back into the store.
3. Swapping storage later means changing ONE argument - the factory.

## Persistence options

- `InMemoryChatMessageHistory` (from `langchain_core.chat_history`) - a dict of
  message lists living inside the Python process. Zero setup, dies with the
  process: right for notebooks and demos.
- `SQLChatMessageHistory` (from `langchain_community`) - rows in SQLite/Postgres
  keyed by session id; conversations survive restarts and can be inspected with
  any SQL client. The notebook proves the round trip against
  `DATA / "chat.sqlite"` behind a guard.
- Anything else implementing `BaseChatMessageHistory` (Redis, files) plugs into
  the same factory slot - learn the pattern once.

## Common pitfalls

- **Unbounded history cost**: buffer memory resends EVERY old turn on EVERY call;
  token spend grows quadratically over a long chat until the model's context
  window hard-fails. Trim (window) or summarize for anything user-facing.
- **Cross-session leakage**: building one shared history object instead of a
  per-id factory means user A's name shows up in user B's answers. Always key by
  session id, and prove isolation with two sessions answering differently.
- **Windows dropping critical facts**: trim to the last 4 messages and the name
  from turn 1 vanishes exactly when asked about. Keep critical facts in a system
  message or summary instead of hoping they survive trimming.
- **Wrong wiring**: forgetting `input_messages_key` or `history_messages_key`
  produces confusing KeyError traces - the wrapper must know which dict entry is
  the human input and which placeholder receives history.

## Contents

1. [01_chat_history_memory.ipynb](01_chat_history_memory.ipynb) - char-bloat demo, InMemory histories +
   `RunnableWithMessageHistory`, two-session isolation proof, sliding-window
   trim util with cost math, guarded SQLChatMessageHistory round trip.
2. [02_stateful_chatbot_app.ipynb](02_stateful_chatbot_app.ipynb) - full "librarian of Alice" chatbot:
   persona prompt + history placeholder + capped interactive loop, second-session
   separation demo, transcripts exported to `DATA / "transcripts.json"`.

After this module continue to `12_capstone_rag_chatbot` to combine RAG + memory.

## Summary

Stateless models need YOU to carry the conversation. Store past turns under a
session id, inject them via `RunnableWithMessageHistory`, and budget them with a
window before costs balloon. In-memory stores for learning, SQL when sessions
must outlive the process. Get the wiring right and the capstone chatbot will
remember each reader's questions separately - which is precisely what makes it
feel like a companion rather than a vending machine.
