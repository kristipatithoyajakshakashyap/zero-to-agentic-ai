# Module 11 - Voice Agents

> **MLCourse - Agentic AI - Agent Patterns**

## Concept

A voice agent is not a new kind of agent. It is a **text agent between two
lossy converters**:

```
audio in -> [ STT ] -> text -> [ your agent ] -> text -> [ TTS ] -> audio out
```

Everything you already know about prompts, tools, schemas and memory applies
unchanged to the middle box. What is new is that the input is a *hypothesis* -
the agent never sees what the caller said, only what the transcriber thought
they said - and that one fact reshapes the design.

This module works on **audio files, not a live microphone**, so it runs
headless in a notebook and is fully reproducible. The input audio is
synthesised offline with the operating system's own voice, which also means
the script is known exactly and Word Error Rate can be computed honestly.

## Why it matters

- **Voice is a real deployment surface**: phone support, kiosks, hands-busy
  and eyes-busy contexts, accessibility.
- **The failure mode is specific.** Numbers, IDs, names and spellings are
  what STT gets wrong most often, and they are precisely the values agents
  act on. An agent that acts on an unconfirmed transcript reschedules
  somebody else's delivery.
- **Latency is the product.** On a call, a pause over ~800 ms reads as a
  dropped line. That forces architectural choices (separable stages,
  streaming, short replies) that text agents never have to make.
- **The discipline transfers.** "Pin a schema, `null` instead of guessing,
  confirm before acting, decide consent in code" is the same lesson as the
  browser module in a different medium.

## Provider status: Groq TTS

Groq hosts `canopylabs/orpheus-v1-english` for text-to-speech. **On this
account it returns HTTP 400 `model_terms_required`** - Groq requires an
organisation admin to accept the model's terms once in the Groq console
before any request succeeds. No code can work around it.

So notebook 02 **calls the Groq TTS endpoint on every run and prints the real
HTTP response verbatim**, then produces the audio with `pyttsx3` (the offline
OS voice) so the loop genuinely closes and a real `.wav` is written. If the
terms are accepted for your organisation, the Groq branch takes over with no
code change. Speech-to-text (`whisper-large-v3`) works on Groq with no such
gate and is used for real throughout.

## Notebooks

### `01_speech_to_text.ipynb`
Generating a real `.wav` with no microphone and no network. Calling Groq
`whisper-large-v3` (a multipart upload - a JSON body silently 400s).
`verbose_json` for segments, timings and the `avg_logprob` /
`no_speech_prob` confidence signals that should trigger a confirmation.
Implementing **Word Error Rate** and sanity-checking the metric before
trusting it. The `prompt` parameter for domain vocabulary - reported
honestly: on this clip it changed nothing, because Whisper already resolved
the jargon. The section ends on the more valuable lesson: measured against
the spoken script the WER is 56.7%, against the written form we actually
wanted it is 0.0%. Same transcript, different yardstick.

### `02_voice_agent_loop.ipynb`
The full loop as three independent, separately-timed functions. Why a prompt
written for a screen sounds terrible read aloud, shown side by side. The TTS
step, including the live Groq attempt described above. An inline `IPython`
audio player for both the caller clip and the reply. A measured latency
budget - in the recorded run STT 836 ms / agent 333 ms / TTS 118 ms - plus
the stages the loop never sees (endpointing, network), and why streaming
requires the stages to stay separable.

### `03_intents_and_slots.ipynb`
Turning a transcript into a filled form: intent plus slots, pinned schema,
`null` rather than a guess, and Python validation that `order_number` is
digits. Then the same extraction against a deliberately garbled transcript
("four four seven one" -> "for for seven what") - in the recorded run the
extractor correctly returned `null` and flagged `confidence: low`. Slot-fill
policy that asks about exactly **one** missing value. Finally the
confirmation pattern: read critical values back with digits spelled out, and
gate the action behind a `caller_said_yes` function written in **plain
Python** - consent is control flow, never a model call.

### `04_voice_in_practice.ipynb`
The operational layer. File-size limits and a real silence-based chunker
(RMS over PCM frames) that found 7 clean speech spans in a 23s clip, so no
word is cut at a boundary. Per-second cost modelling on the actual clips.
The full latency table including endpointing. Speaking time as a design
constraint (~150 wpm - a screen-style paragraph takes 20+ seconds to hear).
Where voice is the right interface and where it is actively worse. Voice
specific safety: no audit trail the user can see, voice as biometric data,
and disclosure requirements.

## How to run

```bash
# from the repo root, with the project venv active
jupyter lab 03_agentic_ai/06_agent_patterns/11_voice_agents
```

Run the notebooks in order - notebook 04's cost table reads the clips the
earlier notebooks generated (it skips any that are absent, so it still runs
standalone).

Generated audio lands in `audio/` and is safe to delete and regenerate.

## Prerequisites

- `GROQ_API_KEY` in `03_agentic_ai/.env`. The notebooks read it with a
  walk-up helper; note that the helper returns the **repo root**, so the
  path is `TRACK / "03_agentic_ai" / ".env"`.
- `pyttsx3` (`pip install pyttsx3`) for the offline OS voice. It drives
  SAPI5 on Windows, NSSpeechSynthesizer on macOS, espeak on Linux.
- Models: `whisper-large-v3` (STT) and `qwen/qwen3.8-27b` (chat), both on
  Groq. No OpenAI anywhere.
- Groq free tier is **8000 tokens/minute**; every call in this module has
  exponential backoff on 429 and the clips are a few seconds each.
- No microphone, no speakers and no display are required.

## Related modules

- `05_production_security/01_prompt_injection` - the transcript is untrusted
  input; a spoken injection works exactly as well as a typed one.
- `06_agent_patterns/09_prompt_optimization` - the same "state your
  normalisation before quoting a metric" discipline.
- `06_agent_patterns/10_browser_agents` - "model proposes, code decides" in
  another medium.
- `06_agent_patterns/14_async_human_approval` - approval when the human is
  not on the line.
