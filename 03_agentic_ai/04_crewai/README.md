# CrewAI: Multi-Agent Orchestration

A hands-on journey through CrewAI, the standalone framework for building teams of
AI agents that collaborate on complex tasks through role-based design. Move from
scaffolding a single crew to orchestrating production-grade multi-agent workflows
with custom tools, knowledge, memory, and Flows.

## Categories

### [01_fundamentals](./01_fundamentals/README.md) - CrewAI Fundamentals (5 modules)
The foundation: installation, agent roles and goals, task definitions, process
types, built-in tools, and a mini-capstone research crew. Everything you need to
build a working multi-agent system from scratch.

### [02_advanced_agents](./02_advanced_agents/README.md) - Advanced Agent Features (5 modules)
Extend agents with custom tools, knowledge sources, memory systems, reasoning
strategies, conditional tasks, and multimodal capabilities.

### [03_flows_and_orchestration](./03_flows_and_orchestration/README.md) - Flows and Orchestration (5 modules)
CrewAI Flows: typed state management, persistence, human-in-the-loop gates,
MCP integration, and parallel crew execution.

### [04_production](./04_production/README.md) - Production Readiness (5 modules)
Testing, training, observability, coding agents, CLI workflows, LLM provider
connections, and a full-stack capstone application.

## Learning Path

| # | Module | Category | Teaches |
|---|--------|----------|---------|
| 1 | [01_installation_and_first_crew](./01_fundamentals/01_installation_and_first_crew/README.md) | Fundamentals | pip install, CLI scaffolding, first crew |
| 2 | [02_agents_deep_dive](./01_fundamentals/02_agents_deep_dive/README.md) | Fundamentals | Agent role/goal/backstory, LLM assignment, delegation |
| 3 | [03_tasks_and_processes](./01_fundamentals/03_tasks_and_processes/README.md) | Fundamentals | Tasks, sequential vs hierarchical, async kickoff |
| 4 | [04_built_in_tools](./01_fundamentals/04_built_in_tools/README.md) | Fundamentals | FileReadTool, ScrapeWebsiteTool, SerperDevTool catalog |
| 5 | [05_research_assistant_crew](./01_fundamentals/05_research_assistant_crew/README.md) | Fundamentals | Mini-capstone research crew |
| 1 | [01_custom_tools](./02_advanced_agents/01_custom_tools/README.md) | Advanced Agents | @tool decorator, BaseTool subclass, error handling |
| 2 | [02_knowledge_sources](./02_advanced_agents/02_knowledge_sources/README.md) | Advanced Agents | Text/PDF knowledge, agent vs crew knowledge |
| 3 | [03_memory_systems](./02_advanced_agents/03_memory_systems/README.md) | Advanced Agents | Short-term, long-term, entity memory |
| 4 | [04_reasoning_and_planning](./02_advanced_agents/04_reasoning_and_planning/README.md) | Advanced Agents | Chain-of-thought, crew planning |
| 5 | [05_conditional_and_multimodal](./02_advanced_agents/05_conditional_and_multimodal/README.md) | Advanced Agents | ConditionalTask, VisionTool, DALL-E |
| 1 | [01_flows_basics](./03_flows_and_orchestration/01_flows_basics/README.md) | Flows | Flow class, @start, @listen, typed state |
| 2 | [02_flow_state_persistence](./03_flows_and_orchestration/02_flow_state_persistence/README.md) | Flows | @persist, SQLite checkpointing, resume/fork |
| 3 | [03_human_in_the_loop](./03_flows_and_orchestration/03_human_in_the_loop/README.md) | Flows | @human_feedback, approval gates |
| 4 | [04_mcp_integration](./03_flows_and_orchestration/04_mcp_integration/README.md) | Flows | MCPServerAdapter, transports, security |
| 5 | [05_delegation_and_parallel_crews](./03_flows_and_orchestration/05_delegation_and_parallel_crews/README.md) | Flows | Delegation chains, parallel crews |
| 1 | [01_testing_and_training](./04_production/01_testing_and_training/README.md) | Production | crewai test, crew.train(), evaluation |
| 2 | [02_observability](./04_production/02_observability/README.md) | Production | Tracing, event listeners, OpenTelemetry |
| 3 | [03_coding_agents_and_cli](./04_production/03_coding_agents_and_cli/README.md) | Production | CodeInterpreterTool, AGENTS.md, CLI |
| 4 | [04_llm_connections](./04_production/04_llm_connections/README.md) | Production | LiteLLM, Ollama, Groq, model selection |
| 5 | [05_capstone_full_stack_app_builder](./04_production/05_capstone_full_stack_app_builder/README.md) | Production | Full-stack app builder capstone |

## Prerequisites

- Python 3.10+
- Complete **LangChain Fundamentals** recommended (01_langchain) for context on
  prompts, tools, and chains that CrewAI builds on top of

## Setup

Install CrewAI and its tooling extras:

```powershell
pip install crewai "crewai[tools]"
```

Copy the shared environment file and add your keys:

```powershell
copy .env.example .env       # then paste your Groq/HF/OpenAI keys
```

For the local-first path also install Ollama once:

```powershell
winget install Ollama.Ollama
ollama pull llama3.2
```
