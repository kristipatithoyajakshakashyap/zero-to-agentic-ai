# LangGraph - Graph-Based Agents

A chain runs forward once. An agent needs to loop, branch, pause for a human, and
remember what happened last Tuesday. LangGraph gives you that shape explicitly:
you declare a **state** object, write **nodes** that update it, and connect them
with **edges** — including conditional ones that let the graph decide where to go
next. The result is an agent you can draw, checkpoint, interrupt, and replay.

## The idea in one picture

```
        +------------------ conditional edge ------------------+
        |                                                      |
      START -> [agent node] -> tools? -> [tool node] ----------+
                    |
                    | no more tools
                    v
                 [answer] -> END

  state (a TypedDict) flows through every node
  checkpointer saves it after every step  ->  pause, resume, time-travel
```

Modules 01-03 build that picture piece by piece; 04-06 add the things production
agents need (human approval, streaming output, more than one agent); 07-08 scale
it up (composing graphs out of graphs, and reasoning patterns beyond the ReAct
loop); 09 puts it all into one project.

## Modules (canonical learning order)

| Folder | Step | Teaches |
|---|---|---|
| [01_graph_basics](./01_graph_basics/README.md) | 1 | Why graphs beat chains · `StateGraph`, nodes, edges · conditional routing · state reducers |
| [02_tool_using_agents](./02_tool_using_agents/README.md) | 2 | `@tool` decorator · `ToolNode` and `tools_condition` · ReAct loop · custom agent graphs |
| [03_persistence_checkpointing](./03_persistence_checkpointing/README.md) | 3 | `MemorySaver` · `SqliteSaver`/`PostgresSaver` · time-travel replay · cross-thread memory |
| [04_human_in_the_loop](./04_human_in_the_loop/README.md) | 4 | `interrupt()` and `Command(resume=...)` · approval gates · breakpoints for debugging |
| [05_streaming](./05_streaming/README.md) | 5 | `stream()` vs `invoke()` · token streaming with `astream_events` · streaming multi-node graphs |
| [06_multi_agent_systems](./06_multi_agent_systems/README.md) | 6 | Supervisor pattern · swarm handoff · hierarchical supervisors · parallel agents |
| [07_subgraphs_and_composition](./07_subgraphs_and_composition/README.md) | 7 | Compiled graphs as nodes · shared vs isolated state at the boundary · `Send` for runtime fan-out · composed pipelines |
| [08_advanced_reasoning_patterns](./08_advanced_reasoning_patterns/README.md) | 8 | Where ReAct breaks down · Reflexion · Plan-and-Execute · ReWOO · measured pattern comparison |
| [09_travel_planner](./09_travel_planner/README.md) | 9 | Capstone: research agent + planning agent + human approval gate in one graph |
| [10_state_migration_and_versioning](./10_state_migration_and_versioning/README.md) | 10 | What breaks when the state schema changes · additive vs breaking changes · versioned state and migration chains · recovering old and suspended checkpoints |

Note the dependency order that is not purely linear: human-in-the-loop (04)
requires checkpointing (03), because `interrupt()` can only resume from a saved
checkpoint. Streaming (05) only needs the agent loop from 02. Subgraphs (07) lean
on the state reducers from 01 and the checkpoint namespaces from 03, and the
reasoning patterns in 08 are measured against the ReAct loop from 02.

## Prerequisites

Complete [**01_langchain**](../01_langchain/README.md) first. This track assumes
you are comfortable with chat models, `ChatPromptTemplate`, LCEL piping, and
basic retrieval — LangGraph nodes are ordinary Python functions that usually call
a LangChain chain inside.

## Providers and keys

The course is **local-first with a free cloud fallback**:

- **Ollama** (`ChatOllama`) — free, local, no key. The default in most notebooks,
  and the only model the capstone needs.
- **Groq** (`ChatGroq`) — free-tier cloud key, used where fast inference makes a
  demo (especially streaming) much nicer to watch.

`GROQ_API_KEY` lives in `03_agentic_ai/.env`. In modules 01-06 and 09, cells that
need a key are guarded: if the key is missing they print setup instructions and
skip, so every notebook still runs top-to-bottom.

Modules **07** and **08** invert that default: they are **Groq-first**
(`qwen/qwen3.8-27b`) with local Ollama as the fallback, because their measurements
— token counts, latency, pattern comparisons — only mean something against a real
model. Both use a `safe_invoke` helper that paces calls and backs off on HTTP 429
to stay inside Groq's free-tier limit of roughly 8000 tokens per minute. OpenAI is
never used anywhere in this course.

## Setup

```powershell
copy ..\.env.example ..\.env    # then paste your Groq key
winget install Ollama.Ollama
ollama pull llama3.2
pip install langgraph langchain-ollama langchain-groq langgraph-checkpoint-sqlite
```

## Data and artifacts

This track needs no external corpus — the tools in the notebooks return canned
data so results are reproducible and free. Running the notebooks does create
local artifacts, which are safe to delete:

- `03_persistence_checkpointing/checkpoints.db` — the SQLite checkpoint store
  written by `02_sqlite_postgres.ipynb`. Delete it to start the persistence
  demos from scratch.
