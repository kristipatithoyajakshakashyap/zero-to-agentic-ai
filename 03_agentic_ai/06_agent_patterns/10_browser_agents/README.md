# Module 10 - Browser Agents

> **MLCourse - Agentic AI - Agent Patterns**

## Concept

A **browser agent** is an agent whose tools drive a real web browser: open a
page, read it, click, type, submit. Playwright does the driving; the LLM does
the interpreting and the deciding.

This module teaches the mechanism at its smallest and **entirely offline**.
Every page is a local `.html` fixture the notebooks write to `fixtures/` and
open with a `file://` URL. No network, no live sites, no non-determinism, and
no way to accidentally act on a real service.

## Why it matters

- **Most systems have a web UI and no API.** A browser is the universal
  integration of last resort.
- **It is the most dangerous tool shape in this course.** A browser agent's
  entire job is to read text *somebody else wrote*, and that text lands in
  your prompt next to your instructions. This is indirect prompt injection
  with real tools attached - see notebook 04, and
  `05_production_security/01_prompt_injection` for the general attack class.
- **The design lessons transfer.** "Model decides values, code owns
  selectors", "constrain the output to a set you built", "verify the outcome"
  apply to every tool-using agent, not just browsers.

## Notebooks

### `01_playwright_basics.ipynb`
The three Playwright objects (driver, Browser, Page). Writing local HTML
fixtures and opening them with `file://`. `page.content()` vs
`page.inner_text("body")`, measured - and why the model gets rendered text.
Locators and the preference order (role/label > id > structural CSS).
Screenshots as a debugging tool. Also handles the two Jupyter/Windows quirks
once for the whole module: sync Playwright needs a worker thread inside a
notebook, and Windows needs the Proactor event-loop policy restored.

### `02_llm_reads_a_page.ipynb`
The **fetch -> reduce -> extract** pipeline, kept as three separate steps so
failures are attributable. Reducing a page to the relevant lines before
spending tokens. Pinning a schema in the prompt and validating it in Python
with a loud `assert`. Extracting a policy from *prose*, where no selector can
reach. Then the honest comparison on a structured table: the LLM and the
selector produce identical results, but the selector is faster, free, and
exact. Ends with a token budget against Groq's 8000 TPM limit.

### `03_filling_a_form.ipynb`
The agent acts. Playwright's `fill` / `select_option` / `check` / `click`.
The key safety decision: **the model emits values, never selectors** - you
enumerate the fields, you own the selector table. Validating the model's
values before touching the browser (three assertions, three real failure
modes). An allow-listed executor that refuses unknown keys. Reading the
result *and* the DOM back, because a click that silently did nothing is the
normal failure - Playwright reports success while the page reports an error.

### `04_untrusted_page_text.ipynb`
The most important notebook here. A poisoned local page carrying a visible
injected "system notice" plus a `display:none` payload. The naive agent is
run against it, and whichever way that particular run goes, the notebook is
explicit that a resisted injection proves nothing. Then three mitigations
that actually help - channel separation, constraining the output to a set
your code built, and limiting the capability itself - and several that do
not (blocklists, "ignore instructions in the page", stripping hidden
elements, a stronger model). Closes with a design checklist.

## How to run

```bash
# once, to download the browser binary
python -m playwright install chromium

# from the repo root, with the project venv active
jupyter lab 03_agentic_ai/06_agent_patterns/10_browser_agents
```

Run the notebooks in order. Each is self-contained: it writes the fixtures it
needs, so any notebook can be run on its own.

Generated files - `fixtures/*.html` and `catalog.png` - are written next to
the notebooks and are safe to delete and regenerate.

## Prerequisites

- **Chromium** downloaded via `python -m playwright install chromium`.
- `GROQ_API_KEY` in `03_agentic_ai/.env`. The notebooks read it with a
  walk-up helper; note that the helper returns the **repo root**, so the
  path is `TRACK / "03_agentic_ai" / ".env"`.
- Model: `qwen/qwen3.8-27b` on Groq. No OpenAI anywhere.
- Groq free tier is **8000 tokens/minute**. Every model call in this module
  goes through a helper with exponential backoff on 429, and the pages are
  deliberately tiny.
- Recommended before notebook 04:
  `03_agentic_ai/05_production_security/01_prompt_injection`.

## Related modules

- `05_production_security/01_prompt_injection` - the attack class in general.
- `05_production_security/02_guardrail_frameworks` - validating model output.
- `06_agent_patterns/14_async_human_approval` - doing the approval step
  properly when the human is not at the keyboard.
