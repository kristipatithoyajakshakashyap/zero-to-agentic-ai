# Module 01 - Chat Models and Providers

> **MLCourse - Agentic AI - Chat Models and Providers**

> Stage in the capstone: the generate stage - every answer in the final chatbot comes from one of these engines.

A chat model is the smallest useful unit of any LLM application: a list of typed
messages goes in, exactly one assistant message comes out. Everything else in this
track (prompts, parsers, chains, retrieval, memory) is machinery that wraps around,
feeds, or post-processes that single call. Master it first and the rest of the track
becomes plumbing around a contract you already understand.

## Why chat models are step 1

- Every later module calls a model under the hood. Prompts shape what you send,
  parsers clean what you receive, RAG injects context into the call - but the call
  itself is always "messages in, message out".
- LangChain gives all providers one identical interface (`invoke`, `stream`,
  `batch`, LCEL piping), so you learn the API once and swap engines with a string.
- The track is **local-first**: Ollama costs nothing and keeps data on your machine,
  which is ideal while you are learning and experimenting aggressively.
- Cloud providers (Groq, HuggingFace, OpenAI) exist for speed, model variety, and a
  quality benchmark - each guarded by a key check so notebooks still run without them.

## The four providers compared

| Provider | Cost | Speed | Privacy | Setup |
|---|---|---|---|---|
| Ollama (local) | Free forever | Fast on GPU, usable on CPU for 3B models | Total - nothing leaves your laptop | Install Ollama app, then `ollama pull llama3.2` (~2 GB download) |
| Groq (cloud) | Free tier, rate limited (requests/min + tokens/day caps) | Extreme - custom LPU hardware serves hundreds of tokens/sec | Prompts leave your machine to Groq servers | Free key at console.groq.com into `03_agentic_ai/.env` as `GROQ_API_KEY` |
| HuggingFace hosted | Small free monthly credit, then per-request pricing | Moderate - cold starts and queueing possible | Prompts go to HF or its inference partners | Free `HUGGINGFACEHUB_API_TOKEN` from hf.co/settings/tokens; some repos need license acceptance |
| OpenAI (cloud) | Pay per token (gpt-4o-mini is very cheap) | Fast and reliable | Prompts sent to OpenAI | Paid `OPENAI_API_KEY`; used in exactly ONE notebook of this track |

## When and how to use each

### Ollama - the local-first default

Use it whenever you can: learning, privacy-sensitive text, offline work, unlimited
trial-and-error without watching a quota meter. The trade-off is that throughput
depends on your hardware and you only get open-weight models.

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0.2)
print(llm.invoke("Explain embeddings in one sentence.").content)
```

### Groq - the speed demon

Same open models you run locally, served on custom LPU silicon at extreme tokens/sec.
The free tier is generous enough for the whole course. Watch the rate limits: bursty
loops can return HTTP 429, so keep outputs short in experiments.

```python
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_KEY, max_tokens=100)
```

Best for: fast iteration, snappy demos, running a 70B model you could never host at home.

### HuggingFace - the model zoo

The Hub hosts over a million community models. Hosted inference lets you call rare or
fine-tuned checkpoints over HTTPS with no GPU and no download. You pick a repo id like
`meta-llama/Llama-3.2-3B-Instruct`, accept the license if the repo is gated, and go.
Keyless local alternatives still exist (see the Ollama cross-reference inside the notebook).

```python
from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-3B-Instruct",
                          huggingfacehub_api_token=HF_TOKEN, max_new_tokens=128)
```

### OpenAI - the quality benchmark

GPT models remain the reference point others are compared against. This track uses
OpenAI in exactly one notebook to teach the provider-swap pattern and to give you an
honest baseline; bound your spending with `max_tokens` while experimenting.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=100)
```

## Key parameters cheat sheet

| Parameter | What it does | Notes and gotchas |
|---|---|---|
| `model` | Which checkpoint to run | Names differ per provider: `llama3.2` locally vs `llama-3.3-70b-versatile` on Groq. Must match exactly. |
| `temperature` | Randomness dial, typically 0.0 to 1.5+ | Low (0.0-0.3) for factual RAG answers, mid (0.5-0.8) for general chat, high (1.0+) for brainstorming. |
| Max output cap | Stops runaway generations | Called `num_predict` on `ChatOllama`, `max_new_tokens` on HF endpoints, `max_tokens` on Groq/OpenAI clients. |
| Streaming | Yield tokens as they are generated | Use `.stream()` instead of `.invoke()`; hugely improves perceived latency in UIs. |
| `timeout` | Give up after N seconds | Protects apps from hung cloud calls and cold-started endpoints. |
| `api_key` / `base_url` | Credentials and endpoint override | Load keys from `.env` via python-dotenv; `base_url` enables proxies and self-hosted gateways. |

## Common pitfalls

- Calling before the Ollama server is up or before `ollama pull llama3.2` finished -
  the error appears at `invoke()` time, not at object construction time.
- Model tag typos: `llama3.2` and `llama-3.2` are different strings to different
  providers. Run `ollama list` to see exact local tags.
- Treating free tiers as unlimited: Groq returns HTTP 429 when you exceed rate limits;
  catch it, wait, or switch to a smaller model such as `llama-3.1-8b-instant`.
- Pasting API keys into notebooks. Keys belong in `03_agentic_ai/.env` (gitignored),
  loaded once via the shared dotenv walk-up snippet every notebook uses.
- Assuming parameter names transfer between providers - they mostly do not (see table above).
- Expecting perfect determinism even at `temperature=0`: results are *mostly* stable,
  not bit-for-bit guaranteed, especially on GPUs.
- Forgetting that hosted endpoints can be cold, queued, or gated - wrap cloud calls in
  try/except and print a friendly skip message so notebooks stay runnable end-to-end.

## Contents

1. `01_ollama_local_first.ipynb` - messages in / message out, invoke-stream-batch, the
   temperature experiment, and an `init_chat_model` teaser.
2. `02_groq_fast_inference.ipynb` - free-tier story, guarded key pattern, live token
   streaming, same-prompt temperature sweep, cloud-vs-local timing framing.
3. `03_huggingface_models.ipynb` - picking a `repo_id`, `HuggingFaceEndpoint` demo with
   token guard, keyless local alternative, when hosted inference makes sense.
4. `04_openai_and_abstraction.ipynb` - minimal OpenAI demo plus THE star lesson: one
   identical chain executed against ollama/groq/openai by swapping a provider string.

After this module, continue to `02_prompt_templates` to control WHAT goes into these engines.
