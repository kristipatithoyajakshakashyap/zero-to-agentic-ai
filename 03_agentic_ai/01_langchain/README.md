# LangChain Fundamentals

Build the complete backbone of LLM applications with LangChain: chat models,
prompts, typed outputs, LCEL chains, document ingestion, chunking, embeddings,
vector stores, retrieval, basic RAG, and stateful chatbots with session memory -
finishing with a capstone that chats with your own documents across persistent
sessions.

## The pipeline you are building toward

Every module powers one stage of the final capstone chatbot:

```
INGEST            CHUNK             EMBED           STORE        RETRIEVE
module 05    ->   module 06    ->   module 07   ->   module 08 -> module 09
loaders           strategies       embeddings      chroma/faiss  retrievers
     |                |                |               |            |
     '----------.-----'----------------.---------------.------------.'
                v
         GENERATE + REMEMBER      =  modules 02,03,04 (prompts, pydantic, lcel)
                |                        + module 10 (basic rag)
                v                        + module 11 (memory/state)
        CAPSTONE (module 12): chat with your own documents,
        across named sessions, powered by everything above
```

## Modules (canonical learning order)

| Folder | Step | Teaches |
|---|---|---|
| [01_chat_models_providers](./01_chat_models_providers/README.md) | 1 | Ollama (local-first) · Groq · HuggingFace · OpenAI swap pattern |
| [02_prompt_templates](./02_prompt_templates/README.md) | 2 | ChatPromptTemplate, roles, variables, few-shot |
| [03_output_parsers_pydantic](./03_output_parsers_pydantic/README.md) | 3 | Typed trustworthy output (parsers pt 1) |
| [04_lcel_and_runnables](./04_lcel_and_runnables/README.md) | 4 | Pipe syntax, passthrough/assign/parallel, streaming (parsers pt 2) |
| [05_document_loaders](./05_document_loaders/README.md) | 5 | txt · md · csv · json · pdf · web · directory loaders |
| [06_chunking_strategies](./06_chunking_strategies/README.md) | 6 | character · recursive · token · markdown-aware · code-aware |
| [07_embeddings](./07_embeddings/README.md) | 7 | Free local embedders vs OpenAI (separate notebooks) |
| [08_vector_stores](./08_vector_stores/README.md) | 8 | Chroma and FAISS side-by-side, head-to-head comparison |
| [09_retrievers](./09_retrievers/README.md) | 9 | as_retriever, similarity vs MMR, k/fetch_k |
| [10_basic_rag](./10_basic_rag/README.md) | 10 | Minimal retrieval-augmented generation chain |
| [11_memory_and_state](./11_memory_and_state/README.md) | 11 | Session-id history, RunnableWithMessageHistory |
| [12_capstone_rag_chatbot](./12_capstone_rag_chatbot/README.md) | 12-13 | Everything combined into a document-chat application |

## Provider rules

- **OpenAI appears in exactly two notebooks**: `01/04_openai_and_abstraction.ipynb`
  and `07/02_openai_embeddings.ipynb`. Everywhere else the course runs on
  Ollama (free/local), Groq (free-tier key), or keyless local HuggingFace models.
- Keys live in `03_agentic_ai/.env` (copy `.env.example`). Cells requiring keys
  print setup instructions and skip gracefully when a key is missing, so every
  notebook executes top-to-bottom regardless.

## Setup

```powershell
copy .env.example .env       # then paste your Groq/HF/OpenAI keys
```

For the local-first path also install Ollama once:

```powershell
winget install Ollama.Ollama
ollama pull llama3.2
```
