# MLCourse - Zero to Advanced

A structured, hands-on curriculum covering Data Science Foundations, Machine
Learning, and Agentic AI. Every topic is delivered as Jupyter notebooks with
dense instructional comments, supported by standalone Markdown reference guides
per section.

## Repository layout

```
MLCourse/
├── 0_data_science_foundations/     NumPy · Pandas · Matplotlib · Seaborn
│                                    + Data Preprocessing + Capstone Projects
├── 02_machine_learning/
│   ├── data/                        shared dataset hub (auto-downloaded)
│   ├── 0_supervised/
│   │   ├── 0_classification/       logistic · knn · svm · naive bayes
│   │   │                            · decision tree · random forest
│   │   │                            · adaboost · gradient boosting · xgboost
│   │   └── 02_regression/           linear (+ Ridge/Lasso/ElasticNet) · knn
│   │                                · svr · decision tree · random forest
│   │                                · adaboost · gradient boosting · xgboost
│   └── 02_unsupervised/             k-means · hierarchical clustering
│                                    · silhouette evaluation lab
└── 03_agentic_ai/
    ├── 01_langchain/                LangChain fundamentals (12 modules):
    │   ├── 01_chat_models_providers     chat models, providers
    │   ├── 02_prompt_templates          prompt engineering
    │   ├── 03_output_parsers_pydantic   structured outputs
    │   ├── 04_lcel_and_runnables        LCEL pipelines
    │   ├── 05_document_loaders          document ingestion
    │   ├── 06_chunking_strategies       text splitting
    │   ├── 07_embeddings                vector representations
    │   ├── 08_vector_stores             Chroma, FAISS
    │   ├── 09_retrievers                retrieval patterns
    │   ├── 10_basic_rag                 introductory RAG
    │   ├── 11_memory_and_state          session memory
    │   └── 12_capstone_rag_chatbot      end-to-end RAG chatbot
    ├── 02_langgraph/                LangGraph agents (7 modules):
    │   ├── 01_graph_basics              StateGraph, nodes, edges
    │   ├── 02_tool_using_agents         tool binding, ToolNode
    │   ├── 03_persistence_checkpointing SqliteSaver, threads
    │   ├── 04_human_in_the_loop         breakpoints, human review
    │   ├── 05_streaming                 stream_mode values
    │   ├── 06_multi_agent_systems       supervisor, swarm
    │   └── 07_travel_planner            agentic travel planning
    ├── 03_rag_advanced/             Advanced RAG (10 modules):
    │   ├── 01_hybrid_search             dense + sparse fusion
    │   ├── 02_multimodal_rag            images, tables, text
    │   ├── 03_agentic_rag               agent-driven retrieval
    │   ├── 04_autonomous_rag            self-directed pipelines
    │   ├── 05_corrective_rag            retrieval validation
    │   ├── 06_adaptive_rag              dynamic strategy selection
    │   ├── 07_cache_rag                 semantic caching
    │   ├── 08_vectorless_rag            BM25, keyword-based
    │   ├── 09_persistent_memory_rag     long-term memory
    │   └── 10_rag_evaluation            RAGAS metrics
    └── 04_crewai/                   CrewAI: Multi-Agent Orchestration (20 modules):
        ├── 01_fundamentals/             agents, tasks, crews, tools
        │   ├── 01_installation_and_first_crew
        │   ├── 02_agents_deep_dive
        │   ├── 03_tasks_and_processes
        │   ├── 04_built_in_tools
        │   └── 05_research_assistant_crew
        ├── 02_advanced_agents/          custom tools, knowledge, memory
        │   ├── 01_custom_tools
        │   ├── 02_knowledge_sources
        │   ├── 03_memory_systems
        │   ├── 04_reasoning_and_planning
        │   └── 05_conditional_and_multimodal
        ├── 03_flows_and_orchestration/  flows, HITL, MCP, parallel crews
        │   ├── 01_flows_basics
        │   ├── 02_flow_state_persistence
        │   ├── 03_human_in_the_loop
        │   ├── 04_mcp_integration
        │   └── 05_delegation_and_parallel_crews
        └── 04_production/               testing, observability, capstone
            ├── 01_testing_and_training
            ├── 02_observability
            ├── 03_coding_agents_and_cli
            ├── 04_llm_connections
            └── 05_capstone_full_stack_app_builder
```

## Environment setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Select the `.venv` Python kernel inside Jupyter so notebooks resolve the
installed packages. If script activation is blocked, run
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.

## Learning path

Work top-to-bottom within each track. Times assume focused part-time study.

| Order | Section | Time | Outcome |
|---|---|---|---|
| **Data Science Foundations** | | | |
| 1 | [NumPy](01_data_science_foundations/01_numpy/) | ~6 h | Arrays, broadcasting, vectorization |
| 2 | [Pandas](01_data_science_foundations/02_pandas/) | ~8 h | Cleaning, groupby, merging, time series |
| 3 | [Matplotlib](01_data_science_foundations/03_matplotlib/) | ~5 h | Full plotting control, dashboards |
| 4 | [Seaborn](01_data_science_foundations/04_seaborn/) | ~5 h | Statistical graphics |
| 5 | [Data Preprocessing](01_data_science_foundations/05_data_preprocessing/) | ~6 h | Missing/numeric/categorical/text pipelines |
| 6 | [Capstone Projects](01_data_science_foundations/06_capstone_projects/) | ~0 h | Five end-to-end projects |
| **Machine Learning** | | | |
| 7 | [Classification](02_machine_learning/01_supervised/01_classification/) | ~6 h | Nine classifiers with graded projects |
| 8 | [Regression](02_machine_learning/01_supervised/02_regression/) | ~3 h | Eight regressors with graded projects |
| 9 | [Unsupervised Learning](02_machine_learning/02_unsupervised/) | ~6 h | Clustering plus silhouette evaluation |
| **LangChain** | | | |
| 10 | [Chat Models & Providers](03_agentic_ai/01_langchain/01_chat_models_providers/) | ~4 h | Chat models, providers |
| 11 | [Prompt Templates](03_agentic_ai/01_langchain/02_prompt_templates/) | ~3 h | Prompt engineering |
| 12 | [Output Parsers & Pydantic](03_agentic_ai/01_langchain/03_output_parsers_pydantic/) | ~3 h | Structured outputs |
| 13 | [LCEL & Runnables](03_agentic_ai/01_langchain/04_lcel_and_runnables/) | ~4 h | LCEL pipelines |
| 14 | [Document Loaders](03_agentic_ai/01_langchain/05_document_loaders/) | ~3 h | Document ingestion |
| 15 | [Chunking Strategies](03_agentic_ai/01_langchain/06_chunking_strategies/) | ~3 h | Text splitting |
| 16 | [Embeddings](03_agentic_ai/01_langchain/07_embeddings/) | ~3 h | Vector representations |
| 17 | [Vector Stores](03_agentic_ai/01_langchain/08_vector_stores/) | ~4 h | Chroma, FAISS |
| 18 | [Retrievers](03_agentic_ai/01_langchain/09_retrievers/) | ~3 h | Retrieval patterns |
| 19 | [Basic RAG](03_agentic_ai/01_langchain/10_basic_rag/) | ~4 h | Introductory RAG |
| 20 | [Memory & State](03_agentic_ai/01_langchain/11_memory_and_state/) | ~4 h | Session memory |
| 21 | [RAG Chatbot Capstone](03_agentic_ai/01_langchain/12_capstone_rag_chatbot/) | ~4 h | End-to-end RAG chatbot |
| **LangGraph** | | | |
| 22 | [Graph Basics](03_agentic_ai/02_langgraph/01_graph_basics/) | ~4 h | StateGraph, nodes, edges |
| 23 | [Tool-Using Agents](03_agentic_ai/02_langgraph/02_tool_using_agents/) | ~4 h | Tool binding, prebuilt ToolNode agents |
| 24 | [Persistence & Checkpointing](03_agentic_ai/02_langgraph/03_persistence_checkpointing/) | ~4 h | SqliteSaver, thread management, state replay |
| 25 | [Human-in-the-Loop](03_agentic_ai/02_langgraph/04_human_in_the_loop/) | ~3 h | Breakpoints, interrupt_before, human review |
| 26 | [Streaming](03_agentic_ai/02_langgraph/05_streaming/) | ~3 h | stream_mode values, token/event streaming |
| 27 | [Multi-Agent Systems](03_agentic_ai/02_langgraph/06_multi_agent_systems/) | ~4 h | Supervisor, swarm, agent handoffs |
| 28 | [Travel Planner](03_agentic_ai/02_langgraph/07_travel_planner/) | ~4 h | Agentic travel planning with tools |
| **RAG Advanced** | | | |
| 29 | [Hybrid Search](03_agentic_ai/03_rag_advanced/01_hybrid_search/) | ~4 h | Dense + sparse retrieval fusion |
| 30 | [Multi-Modal RAG](03_agentic_ai/03_rag_advanced/02_multimodal_rag/) | ~4 h | Images, tables, and text in RAG |
| 31 | [Agentic RAG](03_agentic_ai/03_rag_advanced/03_agentic_rag/) | ~4 h | Agent-driven retrieval and reasoning |
| 32 | [Autonomous RAG](03_agentic_ai/03_rag_advanced/04_autonomous_rag/) | ~3 h | Self-directed retrieval pipelines |
| 33 | [Corrective RAG](03_agentic_ai/03_rag_advanced/05_corrective_rag/) | ~4 h | Retrieval validation and correction |
| 34 | [Adaptive RAG](03_agentic_ai/03_rag_advanced/06_adaptive_rag/) | ~3 h | Dynamic strategy selection |
| 35 | [Cache RAG](03_agentic_ai/03_rag_advanced/07_cache_rag/) | ~3 h | Semantic caching for RAG |
| 36 | [Vectorless RAG](03_agentic_ai/03_rag_advanced/08_vectorless_rag/) | ~4 h | BM25 and keyword-based RAG |
| 37 | [Persistent Memory RAG](03_agentic_ai/03_rag_advanced/09_persistent_memory_rag/) | ~3 h | Long-term memory across sessions |
| 38 | [RAG Evaluation](03_agentic_ai/03_rag_advanced/10_rag_evaluation/) | ~4 h | Faithfulness, relevance, RAGAS metrics |
| **CrewAI** | | | |
| 39 | [Installation & First Crew](03_agentic_ai/04_crewai/01_fundamentals/01_installation_and_first_crew/) | ~3 h | CrewAI setup, first agent-team |
| 40 | [Agents Deep Dive](03_agentic_ai/04_crewai/01_fundamentals/02_agents_deep_dive/) | ~3 h | Role, goal, backstory, LLM assignment |
| 41 | [Tasks & Processes](03_agentic_ai/04_crewai/01_fundamentals/03_tasks_and_processes/) | ~3 h | Sequential vs hierarchical, async |
| 42 | [Built-in Tools](03_agentic_ai/04_crewai/01_fundamentals/04_built_in_tools/) | ~3 h | 40+ tool catalog |
| 43 | [Research Assistant](03_agentic_ai/04_crewai/01_fundamentals/05_research_assistant_crew/) | ~3 h | Mini-capstone research crew |
| 44 | [Custom Tools](03_agentic_ai/04_crewai/02_advanced_agents/01_custom_tools/) | ~3 h | @tool, BaseTool, hooks |
| 45 | [Knowledge Sources](03_agentic_ai/04_crewai/02_advanced_agents/02_knowledge_sources/) | ~3 h | Text/PDF knowledge, RAG |
| 46 | [Memory Systems](03_agentic_ai/04_crewai/02_advanced_agents/03_memory_systems/) | ~3 h | Short/long-term, entity memory |
| 47 | [Reasoning & Planning](03_agentic_ai/04_crewai/02_advanced_agents/04_reasoning_and_planning/) | ~3 h | Chain-of-thought, crew planning |
| 48 | [Conditional & Multimodal](03_agentic_ai/04_crewai/02_advanced_agents/05_conditional_and_multimodal/) | ~3 h | ConditionalTask, VisionTool |
| 49 | [Flows Basics](03_agentic_ai/04_crewai/03_flows_and_orchestration/01_flows_basics/) | ~3 h | @start, @listen, typed state |
| 50 | [Flow State Persistence](03_agentic_ai/04_crewai/03_flows_and_orchestration/02_flow_state_persistence/) | ~3 h | @persist, SQLite checkpointing |
| 51 | [Human-in-the-Loop](03_agentic_ai/04_crewai/03_flows_and_orchestration/03_human_in_the_loop/) | ~3 h | @human_feedback, approval gates |
| 52 | [MCP Integration](03_agentic_ai/04_crewai/03_flows_and_orchestration/04_mcp_integration/) | ~3 h | MCPServerAdapter, transports |
| 53 | [Delegation & Parallel Crews](03_agentic_ai/04_crewai/03_flows_and_orchestration/05_delegation_and_parallel_crews/) | ~3 h | Supervisor, fan-out/fan-in |
| 54 | [Testing & Training](03_agentic_ai/04_crewai/04_production/01_testing_and_training/) | ~3 h | crewai test, crew.train() |
| 55 | [Observability](03_agentic_ai/04_crewai/04_production/02_observability/) | ~3 h | Tracing, event listeners |
| 56 | [Coding Agents & CLI](03_agentic_ai/04_crewai/04_production/03_coding_agents_and_cli/) | ~3 h | CodeInterpreter, AGENTS.md |
| 57 | [LLM Connections](03_agentic_ai/04_crewai/04_production/04_llm_connections/) | ~3 h | LiteLLM, Ollama, Groq |
| 58 | [Full-Stack App Builder](03_agentic_ai/04_crewai/04_production/05_capstone_full_stack_app_builder/) | ~6 h | 6-agent capstone with Flow orchestration |

Study discipline matters more than speed: read the section reference first,
execute every cell, attempt exercises before solutions, and inspect errors
deliberately.

## Datasets

All data is real. Seaborn built-ins, sklearn loaders, and stable public mirrors
are fetched by download-once helpers inside the notebooks and cached locally;
the machine-learning track consolidates them under `02_machine_learning/data/`.
After the initial fetches the entire course runs offline.

## Troubleshooting

| Problem | Resolution |
|---|---|
| Module not found in a notebook | Switch the kernel to this repository's `.venv` Python |
| seaborn dataset fails to load | Connect once; results cache locally afterwards |
| NLTK LookupError | Run the guarded `nltk.download(...)` cell in that notebook |
| Plots do not render | Ensure the `%matplotlib inline` cell executed |
| Notebook behaves inconsistently | Restart the kernel and run all cells in order |

## Note for contributors

Standards that keep this repository maintainable:

. **Notebooks only.** Content ships as self-contained `.ipynb` files; no
   companion `.py` scripts. A notebook is accepted only if it executes
   top-to-bottom from a fresh kernel without errors.
2. **Comment density is part of the contract.** Every non-trivial line or block
   carries an explanatory comment aimed at a learner seeing the concept for the
   first time.
3. **Data handling.** Datasets are never committed. Fetch them at runtime with
   the established download-once helper and store them in the track's `data/`
   directory; synthetic arrays may appear only to illustrate mathematics inside
   theory notebooks.
4. **Module structure.** New algorithm modules follow the existing layout:
   `README.md` reference, theory notebook, development-workflow notebook, and
   three-to-four graded project notebooks ordered by difficulty.
5. **Documentation sync.** Adding or renaming a module requires updating the
   affected section README and the learning-path table above in the same change.

Keep prose plain, precise, and free of decoration; clarity is the product.
