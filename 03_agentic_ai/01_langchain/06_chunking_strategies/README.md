# [Step 6 - Chunking Strategies] Cutting text so retrieval can win

> **MLCourse - Agentic AI - Module 06: Chunking Strategies**

> Stage in the capstone: stage 2 CHUNK: chunk quality decides retrieval accuracy in the capstone.

## What you'll learn

- why the chunk boundary - not the model - often decides RAG accuracy
- how overlap works, why it exists, and what it costs when overused
- how to reason about chunk SIZE as a precision-versus-completeness dial
- which splitter fits which document kind, and how to decide in minutes

## 1. Why chunking decides RAG quality

Retrieval never sees your documents. It sees CHUNKS - the fragments you cut
yesterday, embedded today, and searched tomorrow. Three consequences follow:

- **The chunk is the unit of similarity.** An embedding summarizes one chunk.
  If a chunk mixes five topics, its single embedding muddles all five and the
  retriever cannot rank it precisely for any of them.
- **The chunk is the unit of context.** Whatever the retriever finds, the LLM
  reads. A chunk that slices a sentence in half feeds the model half a fact -
  confidently retrieved, wrongly stated.
- **The chunk is the unit of cost.** Every retrieved chunk spends context-window
  tokens on every single query. Sloppy sizing is a silent bill.

So chunking is not preprocessing trivia. It defines the atoms of truth your
whole application can express.

## 2. Overlap theory

Overlap repeats the tail of one chunk at the head of the next. With
`chunk_size=500` and `chunk_overlap=100` the arithmetic is fixed:

```text
stride = chunk_size - overlap = 400 new characters per chunk

chunk 1 covers [0    .. 500 ]
chunk 2 covers [400  .. 900 ]   <- 100 chars shared with chunk 1
chunk 3 covers [800  .. 1300]   <- 100 chars shared with chunk 2
```

**Why overlap exists:** a fact that straddles a cut would otherwise appear
half-hidden in two chunks, each unintelligible alone. The shared band lets at
least one chunk contain the WHOLE fact, so retrieval can score it properly.
Think of it as a safety net under the knife.

**The cost of too much overlap:**

- storage grows: overlap `o` on size `s` inflates your index by roughly
  `o / (s - o)` percent - 100/400 means +33 percent vectors to embed and pay for;
- near-duplicate chunks retrieve together, crowding out diverse evidence in
  top-k results;
- repeated context wastes prompt tokens on every query for no new information.

Rule of thumb: 10 to 20 percent of chunk size (50-100 overlap on 500-sized
chunks). More than that buys duplication, not recall.

## 3. Size trade-offs: precision versus completeness

| Chunk size | Retrieval precision | Context completeness | Typical use |
|---|---|---|---|
| small (about 100-300 chars) | high - embeddings stay sharply on-topic | low - facts lose surrounding nuance | FAQ matching, metadata-heavy lookup |
| medium (about 300-800 chars) | balanced | balanced | general RAG over prose - the usual default |
| large (about 1000+ chars) | low - embeddings blur many topics | high - full arguments arrive intact | summarization-style tasks, long-form QA |

Two dials interact with size:

- **overlap** smooths boundaries (see section 2);
- **structure-aware splitting** (headers, code units) lets you keep semantic
  completeness WITHOUT paying for huge blurred chunks - usually the best lever.

## 4. Strategy comparison matrix

| Strategy | Splits on | Respects meaning? | Best for | Watch out |
|---|---|---|---|---|
| CharacterTextSplitter | one fixed separator (e.g. `"\n\n"`) | only if separator matches structure | uniformly paragraphed text | no fallback - missing separator yields oversized chunks; warns "longer than specified" |
| RecursiveCharacterTextSplitter | hierarchy `["\n\n", "\n", " ", ""]` | yes - coarsest structure that fits | the DEFAULT for prose | packs tightly, so it cuts inside paragraphs more often than pure paragraph splitting |
| TokenTextSplitter | tokenizer boundaries (`cl100k_base` etc.) | no - pure budget control | LLM context budgets, billing-sensitive apps | ignores sentences entirely; highest mid-sentence cut rate |
| MarkdownHeaderTextSplitter | ATX headers (`#`, `##`, `###`) | yes - sections stay whole, lineage lands in metadata | docs, wikis, manuals | no size control alone - pair with a size splitter afterwards |
| Code-aware (`RecursiveCharacterTextSplitter.from_language`) | language syntax: `def`, `class`, blocks | yes - functions/classes stay intact | source code, config scripts | very long functions still overflow; blank-line-free code is exactly where it shines |

## 5. Decision guide

```text
What are you cutting?
|
|-- markdown with headers?
|     |-- YES --> MarkdownHeaderTextSplitter, THEN a size splitter per section
|     |-- NO ---> keep going
|
|-- source code?
|     |-- YES --> RecursiveCharacterTextSplitter.from_language(Language.X, ...)
|     |-- NO ---> keep going
|
|-- must chunks fit a token budget exactly?
|     |-- YES --> TokenTextSplitter(encoding_name="cl100k_base", ...)
|     |-- NO ---> keep going
|
|-- prose with reliable blank lines AND flexible sizes?
|     |-- YES --> CharacterTextSplitter("\n\n", ...) is fine
|     |-- NO  --> RecursiveCharacterTextSplitter(size, overlap)  <-- the default answer
|
'--> whatever you chose: inspect chunk boundaries before shipping
    (module notebooks all end with a mid-sentence cut report)
```

## 6. Pitfalls

- **Pitfall - splitting mid-sentence in prose**: a retrieval hit that ends
  halfway through its own punchline poisons generation. Every chunking notebook
  here reports the percentage of chunks NOT ending in terminal punctuation -
  watch that number drop as strategies get smarter.
- **Pitfall - letting tables drift away from their headers**: a size splitter
  cheerfully severs a table row from its column names. Keep tables (and their
  captions) in one chunk, even if that chunk overshoots the target size.
- **Pitfall - thinking in characters when models bill in tokens**: 500 characters
  is roughly 125 tokens of English - but code, German, or non-Latin scripts shift
  that ratio wildly. When a context window or an invoice is involved, split and
  measure in TOKENS (notebook 03).
- **Pitfall - one strategy everywhere**: a settings file, a novel, and an API
  dump want different cutters. Route by document kind; the capstone ingests
  user-supplied files precisely because variety is the norm.

## 7. Contents

| Notebook | Teaches |
|---|---|
| [01_character_splitting.ipynb](01_character_splitting.ipynb) | separator mechanics, overlap arithmetic, the no-fallback trap |
| [02_recursive_splitting.ipynb](02_recursive_splitting.ipynb) | separator hierarchy walkthrough, the sensible default |
| [03_token_splitting.ipynb](03_token_splitting.ipynb) | thinking in tokens, `cl100k_base`, budget-driven sizes |
| [04_markdown_header_aware.ipynb](04_markdown_header_aware.ipynb) | structure-aware splits, header lineage metadata |
| [05_code_aware_splitting.ipynb](05_code_aware_splitting.ipynb) | language-aware splitting, keeping functions whole |
| [06_strategy_comparison.ipynb](06_strategy_comparison.ipynb) | all strategies on one slice, one honest scoreboard |

## Summary

- Chunk quality bounds RAG quality: the retriever can never be smarter than
  the fragments it searches.
- Overlap is insurance against boundary-straddling facts - buy 10-20 percent,
  not more.
- Size is a precision-completeness dial; structure-aware splitters let you
  cheat the trade-off in their domain.
- Default to `RecursiveCharacterTextSplitter`, specialize for markdown, code,
  or token budgets, and always measure boundary damage before shipping.
