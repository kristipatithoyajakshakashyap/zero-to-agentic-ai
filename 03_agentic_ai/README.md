# Track 03 - Agentic AI

A hands-on journey from LangChain basics to advanced RAG and graph-based agents.
The track is split into three progressive categories, each building on the
previous one.

## Categories

### [01_langchain](./01_langchain/README.md) - LangChain Fundamentals (12 modules)
The foundation: chat models, prompts, typed outputs, LCEL chains, document
ingestion, chunking, embeddings, vector stores, retrieval, basic RAG, and
stateful chatbots. Everything you need to build a working document-chat
application.

### [02_langgraph](./02_langgraph/README.md) - LangGraph: Graph-Based Agents (7 modules)
Move beyond linear chains into stateful, graph-based agent workflows: `StateGraph`
basics, tool-using ReAct agents, checkpointing and time-travel, human-in-the-loop
interrupts, streaming, multi-agent topologies, and a travel-planner capstone.

### [03_rag_advanced](./03_rag_advanced/README.md) - Advanced RAG Techniques (10 modules)
Production-grade retrieval: hybrid (BM25 + dense) search, multi-modal RAG,
agentic and autonomous retrieval loops, corrective and adaptive pipelines,
semantic caching, vectorless retrieval with guardrails, persistent memory, and
systematic evaluation.

### [04_crewai](./04_crewai/README.md) - CrewAI: Multi-Agent Orchestration (4 phases, 20 modules)
Standalone multi-agent framework, organised into four phases of five modules
each: `01_fundamentals`, `02_advanced_agents`, `03_flows_and_orchestration`, and
`04_production`. Covers agents, tasks, crews, flows, tools, knowledge, memory,
reasoning, MCP integration, testing, observability, and a full-stack app builder
capstone.

### [05_production_security](./05_production_security/README.md) - Production Security (5 modules)
Security, guardrails, caching, and privacy patterns for production agents.
Conceptual and practical: every module runs deterministically without an API
key. Focuses on the concepts and how to use them (authentication is out of
scope by design).

## Learning Path

| # | Module | Category | Teaches |
|---|--------|----------|---------|
| 1 | [01_chat_models_providers](./01_langchain/01_chat_models_providers/README.md) | LangChain | Ollama · Groq · HuggingFace · OpenAI swap pattern |
| 2 | [02_prompt_templates](./01_langchain/02_prompt_templates/README.md) | LangChain | ChatPromptTemplate, roles, variables, few-shot |
| 3 | [03_output_parsers_pydantic](./01_langchain/03_output_parsers_pydantic/README.md) | LangChain | Typed trustworthy output |
| 4 | [04_lcel_and_runnables](./01_langchain/04_lcel_and_runnables/README.md) | LangChain | Pipe syntax, passthrough/assign/parallel, streaming |
| 5 | [05_document_loaders](./01_langchain/05_document_loaders/README.md) | LangChain | txt · md · csv · json · pdf · web · directory loaders |
| 6 | [06_chunking_strategies](./01_langchain/06_chunking_strategies/README.md) | LangChain | character · recursive · token · markdown-aware · code-aware |
| 7 | [07_embeddings](./01_langchain/07_embeddings/README.md) | LangChain | Free local embedders vs OpenAI |
| 8 | [08_vector_stores](./01_langchain/08_vector_stores/README.md) | LangChain | Chroma and FAISS side-by-side |
| 9 | [09_retrievers](./01_langchain/09_retrievers/README.md) | LangChain | as_retriever, similarity vs MMR, k/fetch_k |
| 10 | [10_basic_rag](./01_langchain/10_basic_rag/README.md) | LangChain | Minimal RAG chain |
| 11 | [11_memory_and_state](./01_langchain/11_memory_and_state/README.md) | LangChain | Session-id history, RunnableWithMessageHistory |
| 12 | [12_capstone_rag_chatbot](./01_langchain/12_capstone_rag_chatbot/README.md) | LangChain | Document-chat application |
| 13 | [01_graph_basics](./02_langgraph/01_graph_basics/README.md) | LangGraph | Why graphs beat chains, StateGraph, nodes/edges, conditional routing, reducers |
| 14 | [02_tool_using_agents](./02_langgraph/02_tool_using_agents/README.md) | LangGraph | @tool, ToolNode, tools_condition, ReAct loop, custom agent graphs |
| 15 | [03_persistence_checkpointing](./02_langgraph/03_persistence_checkpointing/README.md) | LangGraph | MemorySaver, SqliteSaver/PostgresSaver, time travel, cross-thread memory |
| 16 | [04_human_in_the_loop](./02_langgraph/04_human_in_the_loop/README.md) | LangGraph | interrupt()/Command(resume), approval gates, breakpoints |
| 17 | [05_streaming](./02_langgraph/05_streaming/README.md) | LangGraph | stream() vs invoke(), token streaming, streaming multi-node graphs |
| 18 | [06_multi_agent_systems](./02_langgraph/06_multi_agent_systems/README.md) | LangGraph | Supervisor, swarm handoff, hierarchical supervisors, parallel agents |
| 19 | [09_travel_planner](./02_langgraph/09_travel_planner/README.md) | LangGraph | Capstone: research + planning agents behind a human approval gate |
| 20 | [01_hybrid_search](./03_rag_advanced/01_hybrid_search/README.md) | Advanced RAG | BM25, dense retrieval, reciprocal rank fusion, hybrid pipeline |
| 21 | [02_multimodal_rag](./03_rag_advanced/02_multimodal_rag/README.md) | Advanced RAG | Image-text embeddings, multimodal indexing, cross-modal retrieval |
| 22 | [03_agentic_rag](./03_rag_advanced/03_agentic_rag/README.md) | Advanced RAG | Agent-driven retrieval, self-querying, query decomposition |
| 23 | [04_autonomous_rag](./03_rag_advanced/04_autonomous_rag/README.md) | Advanced RAG | Self-routing, self-correction, autonomous reasoning loop |
| 24 | [05_corrective_rag](./03_rag_advanced/05_corrective_rag/README.md) | Advanced RAG | Retrieval grading, hallucination detection, corrective generation |
| 25 | [06_adaptive_rag](./03_rag_advanced/06_adaptive_rag/README.md) | Advanced RAG | Query classification, per-query strategy selection |
| 26 | [07_cache_rag](./03_rag_advanced/07_cache_rag/README.md) | Advanced RAG | Semantic caching, cache invalidation, multi-level cache |
| 27 | [08_vectorless_rag](./03_rag_advanced/08_vectorless_rag/README.md) | Advanced RAG | Page-index retrieval, structured metadata filtering, guardrails |
| 28 | [09_persistent_memory_rag](./03_rag_advanced/09_persistent_memory_rag/README.md) | Advanced RAG | Long-term memory, conversational RAG, cross-session knowledge |
| 29 | [10_rag_evaluation](./03_rag_advanced/10_rag_evaluation/README.md) | Advanced RAG | Metrics, RAGAS framework, human evaluation protocols |
| 30 | [01_prompt_injection](./05_production_security/01_prompt_injection/README.md) | Security | Injection attacks and defenses, detector without keys |
| 31 | [02_guardrail_frameworks](./05_production_security/02_guardrail_frameworks/README.md) | Security | Input/output/action guardrails, Pydantic, fail-closed |
| 32 | [03_caching_strategies](./05_production_security/03_caching_strategies/README.md) | Security | Exact/semantic/TTL cache, poisoning, cache-busting |
| 33 | [04_privacy_and_data](./05_production_security/04_privacy_and_data/README.md) | Security | PII detection, redaction, minimization |
| 34 | [05_security_evaluation](./05_production_security/05_security_evaluation/README.md) | Security | Red-team harness, recall/precision, scorecard |

CrewAI is not numbered in this table because it is a standalone framework you can
pick up at any point after LangChain. Its own twenty modules are listed, in order,
in [04_crewai/README.md](./04_crewai/README.md).

## Data

Shared datasets live in the [`data/`](./data) directory at the root of this
track — including `alice.txt` (the default text corpus),
`attention_is_all_you_need.pdf`, `winequality-red.csv`, and `multimodal_images/`.
Notebooks locate it by walking up to the track root, so run them from wherever
they live. CrewAI keeps its own fixtures in `04_crewai/data/`.

## Prerequisites

- **LangChain modules**: Python 3.10+, basic familiarity with LLMs
- **LangGraph modules**: Complete LangChain Fundamentals first
- **Advanced RAG modules**: Complete LangChain Fundamentals first
- **CrewAI modules**: Complete LangChain Fundamentals first; LangGraph helps but
  is not required
- **Production Security modules**: none — every notebook runs deterministically
  without an API key

## Setup

```powershell
copy .env.example .env       # then paste your Groq/HF/OpenAI keys
```

For the local-first path also install Ollama once:

```powershell
winget install Ollama.Ollama
ollama pull llama3.2
```
