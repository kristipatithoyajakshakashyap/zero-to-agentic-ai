# Module 13 - Framework Landscape (AutoGen on Groq)

> **MLCourse - Agentic AI - Agent Patterns**

## Concept

You have already built agents three ways in this course: **LangChain**
chains, **LangGraph** graphs, and **CrewAI** crews. This module adds a
fourth - **AutoGen** (Microsoft) - and, more importantly, solves the *same
task* in AutoGen and LangGraph inside one notebook, with CrewAI's own working
implementation from elsewhere in this repo referenced directly, so the
comparison is grounded in running code rather than a feature table.

AutoGen's organising idea is different from the rest: agents are
**conversational participants**. You do not draw a graph or assign a
sequential process - you put agents in a room and declare a **termination
condition** for when the conversation should stop.

## Why it matters

- **Frameworks differ mainly in who owns the control flow.** LangGraph makes
  it explicit (a graph you draw). CrewAI derives it from roles and a process.
  AutoGen makes it emergent (a conversation with a stopping rule). Knowing
  which is which tells you what each one hides.
- **Termination is the load-bearing design decision in AutoGen**, and it is
  the one beginners skip. A team with only a semantic stopping rule
  ("APPROVED") can run forever if the model never says the word.
- **Conversational cost is quadratic.** Every turn re-sends the whole
  transcript. This module measures it, not just states it.
- **Choosing "no framework"** is a legitimate answer this module argues for
  explicitly, once you can see what each abstraction is actually buying you.

## Provider note

Every notebook here calls Groq's **OpenAI-compatible endpoint**
(`base_url="https://api.groq.com/openai/v1"`) through AutoGen's own OpenAI
client - there is no Groq-specific AutoGen client, and none is needed. Model:
`qwen/qwen3.8-27b`. **The OpenAI Agents SDK is excluded** from this course by
constraint (it requires OpenAI as the provider); AutoGen is not affected by
that constraint because it talks to Groq through the compatible endpoint.

## Notebooks

### `01_autogen_basics.ipynb`
Pointing `OpenAIChatCompletionClient` at Groq. Why `model_info` is
**mandatory** for a model AutoGen has no built-in capability table for - the
notebook triggers the `ValueError` deliberately so you recognise it later.
`AssistantAgent`, `run()`, and the `TaskResult` message list as AutoGen's
state. Streaming with `run_stream()` and the type-check every stream loop
needs. Agent memory persisting across `run()` calls, and `on_reset()`.

### `02_multi_agent_conversation.ipynb`
Writer and critic in a `RoundRobinGroupChat`. Termination conditions and
composing them with `|` - the recorded run converged cleanly
(`stop_reason: Text 'APPROVED' mentioned`, 3 messages) - but the notebook is
explicit that a semantic condition alone is not safe and every team needs a
mechanical `MaxMessageTermination` backstop. Reading the transcript's
per-message token usage and watching prompt tokens grow turn over turn -
the quadratic cost of the conversational model.

### `03_tools_in_autogen.ipynb`
Registering a plain Python function as a tool - no decorator, no schema; the
docstring and type hints become the tool description AutoGen shows the
model. Reading the typed tool-call transcript
(`ToolCallRequestEvent` / `ToolCallExecutionEvent`), which is the framework's
real advantage for debugging. `reflect_on_tool_use` as a genuine cost lever
(extra LLM call to phrase the answer vs. returning the raw tool result).
Tool results as untrusted input, and argument validation inside the tool
itself, not the prompt.

### `04_framework_comparison.ipynb`
The same writer/critic task, implemented and **executed** twice in this
notebook - once as an AutoGen team, once as an explicit LangGraph
`StateGraph` with an ASCII-rendered graph and a plain-Python
`should_continue` function you could unit test without an LLM - plus
CrewAI's already-working expression of this shape referenced by file path
(`04_crewai/01_fundamentals/05_research_assistant_crew/research_crew.py`).
A measured cost/time table for the two runs executed here (both converged in
2 LLM calls in the recorded run). A comparison table across LangChain,
LangGraph, CrewAI and AutoGen, a decision procedure, and an honest, scoped
paragraph each on Semantic Kernel (prose only - its Python story centres on
Azure/OpenAI, untested here) and the excluded OpenAI Agents SDK.

## How to run

```bash
# from the repo root, with the project venv active
jupyter lab 03_agentic_ai/06_agent_patterns/13_framework_landscape
```

Each notebook is self-contained and creates its own client(s); run in any
order, though 01 -> 04 builds understanding progressively.

## Prerequisites

- `GROQ_API_KEY` in `03_agentic_ai/.env`. The notebooks read it with a
  walk-up helper; note that the helper returns the **repo root**, so the
  path is `TRACK / "03_agentic_ai" / ".env"`.
- `autogen-agentchat` and `autogen-ext` (installed in the project venv).
- `langchain-groq` and `langgraph` for notebook 04's LangGraph comparison
  (already used earlier in this course).
- Groq free tier is **8000 tokens/minute**, shared across concurrently
  running agents in this environment. Every client caps `max_tokens=500`,
  every team has a `MaxMessageTermination` backstop, and the shared task is
  a 2-sentence summary - deliberately tiny.
- AutoGen's API is asynchronous; the notebooks `await` at the top level of
  Jupyter cells (works natively) and always `await client.close()` at the
  end to release the HTTP session.

## Related modules

- `02_langgraph/06_multi_agent_systems` - the graph-native version of
  supervisor/swarm/parallel patterns this module's teams echo.
- `04_crewai/01_fundamentals/05_research_assistant_crew` - the CrewAI
  implementation of this exact task shape, referenced directly above.
- `06_agent_patterns/06_multi_agent_debate` - when multiple agents actually
  outperform one, measured.
- `06_agent_patterns/09_prompt_optimization` - the argument against the
  hand-written `role`/`goal`/`backstory` prompt text CrewAI leans on.
