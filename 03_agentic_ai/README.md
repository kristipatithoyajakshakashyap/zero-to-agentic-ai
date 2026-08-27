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
Move beyond linear chains into stateful, graph-based agent workflows. Branching
logic, cycles, human-in-the-loop, multi-agent systems, and persistent state.

### [03_rag_advanced](./03_rag_advanced/README.md) - Advanced RAG Techniques (10 modules)
Production-grade retrieval: query transformation, hybrid search, reranking,
multi-hop reasoning, knowledge graphs, self-RAG, evaluation, and deployment
patterns.

### [04_crewai](./04_crewai/README.md) - CrewAI: Multi-Agent Orchestration (20 modules)
Standalone multi-agent framework: agents, tasks, crews, flows, tools, knowledge,
memory, reasoning, MCP integration, testing, observability, and a full-stack app
builder capstone.
Production-grade retrieval: query transformation, hybrid search, reranking,
multi-hop reasoning, knowledge graphs, self-RAG, evaluation, and deployment
patterns.

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
| 01 | [01_introduction_to_langgraph](./02_langgraph/01_introduction_to_langgraph/README.md) | LangGraph | StateGraph, nodes, edges, conditional routing |
| 02 | [02_state_management](./02_langgraph/02_state_management/README.md) | LangGraph | TypedState, reducers, channel updates, persistence |
| 03 | [03_tool_calling_agents](./02_langgraph/03_tool_calling_agents/README.md) | LangGraph | ReAct-style agents with tool nodes |
| 04 | [04_human_in_the_loop](./02_langgraph/04_human_in_the_loop/README.md) | LangGraph | Breakpoints, approval nodes, interrupt/resume |
| 05 | [05_multi_agent_systems](./02_langgraph/05_multi_agent_systems/README.md) | LangGraph | Supervisor, swarm, hierarchical topologies |
| 06 | [06_memory_and_persistence](./02_langgraph/06_memory_and_persistence/README.md) | LangGraph | Checkpointers, thread-level state, long-term memory |
| 07 | [07_capstone_agent_app](./02_langgraph/07_capstone_agent_app/README.md) | LangGraph | Full agent application |
| 01 | [01_query_transformations](./03_rag_advanced/01_query_transformations/README.md) | Advanced RAG | HyDE, query rewriting, step-back prompting |
| 02 | [02_advanced_chunking](./03_rag_advanced/02_advanced_chunking/README.md) | Advanced RAG | Semantic and agentic chunking |
| 03 | [03_hybrid_search](./03_rag_advanced/03_hybrid_search/README.md) | Advanced RAG | Dense + sparse retrieval |
| 04 | [04_reranking](./03_rag_advanced/04_reranking/README.md) | Advanced RAG | Cross-encoder reranking, Cohere rerank |
| 05 | [05_multi_hop_rag](./03_rag_advanced/05_multi_hop_rag/README.md) | Advanced RAG | Iterative retrieval, chain-of-thought reasoning |
| 06 | [06_graph_rag](./03_rag_advanced/06_graph_rag/README.md) | Advanced RAG | Knowledge graph augmentation, GraphRAG |
| 07 | [07_self_rag](./03_rag_advanced/07_self_rag/README.md) | Advanced RAG | Self-reflective retrieval, hallucination detection |
| 08 | [08_rag_evaluation](./03_rag_advanced/08_rag_evaluation/README.md) | Advanced RAG | RAGAS, DeepEval, metrics |
| 09 | [09_production_patterns](./03_rag_advanced/09_production_patterns/README.md) | Advanced RAG | Caching, observability, guardrails, streaming |
| 10 | [10_capstone_advanced_rag](./03_rag_advanced/10_capstone_advanced_rag/README.md) | Advanced RAG | End-to-end advanced RAG application |

## Data

Shared datasets live in the `data/` directory at the root of this track.

## Prerequisites

- **LangChain modules**: Python 3.10+, basic familiarity with LLMs
- **LangGraph modules**: Complete LangChain Fundamentals first
- **Advanced RAG modules**: Complete LangChain Fundamentals first

## Setup

```powershell
copy .env.example .env       # then paste your Groq/HF/OpenAI keys
```

For the local-first path also install Ollama once:

```powershell
winget install Ollama.Ollama
ollama pull llama3.2
```
