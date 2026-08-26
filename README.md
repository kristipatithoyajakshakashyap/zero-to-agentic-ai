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
    └── 03_rag_advanced/             Advanced RAG (10 modules):
        ├── 01_hybrid_search             dense + sparse fusion
        ├── 02_multimodal_rag            images, tables, text
        ├── 03_agentic_rag               agent-driven retrieval
        ├── 04_autonomous_rag            self-directed pipelines
        ├── 05_corrective_rag            retrieval validation
        ├── 06_adaptive_rag              dynamic strategy selection
        ├── 07_cache_rag                 semantic caching
        ├── 08_vectorless_rag            BM25, keyword-based
        ├── 09_persistent_memory_rag     long-term memory
        └── 10_rag_evaluation            RAGAS metrics
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
|  | `foundations/0_numpy` | ~6 h | Arrays, broadcasting, vectorization |
| 2 | `foundations/02_pandas` | ~8 h | Cleaning, groupby, merging, time series |
| 3 | `foundations/03_matplotlib` | ~5 h | Full plotting control, dashboards |
| 4 | `foundations/04_seaborn` | ~5 h | Statistical graphics |
| 5 | `foundations/05_preprocessing` | ~6 h | Missing/numeric/categorical/text pipelines |
| 6 | `foundations/06_capstones` | ~0 h | Five end-to-end projects |
| 7 | `ml/classification` | ~6 h | Nine classifiers with graded projects |
| 8 | `ml/regression` | ~3 h | Eight regressors with graded projects |
| 9 | `ml/unsupervised` | ~6 h | Clustering plus silhouette evaluation |
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
