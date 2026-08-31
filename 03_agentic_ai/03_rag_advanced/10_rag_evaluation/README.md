# Module 10: RAG Evaluation

> **MLCourse - RAG Foundations - Quality Measurement**

Systematically evaluate RAG pipelines using retrieval and generation metrics, the RAGAS framework for comprehensive assessment, and human evaluation protocols to benchmark real-world performance.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_evaluation_metrics](01_evaluation_metrics.ipynb) | Core metrics: precision, recall, faithfulness, answer relevance, and context accuracy |
| 02 | [02_ragas_framework](02_ragas_framework.ipynb) | RAGAS framework for automated, reference-free RAG evaluation |
| 03 | [03_human_evaluation](03_human_evaluation.ipynb) | Designing human evaluation protocols, inter-annotator agreement, and scoring rubrics |
| 04 | [04_evaluation_pipeline](04_evaluation_pipeline.ipynb) | Automated evaluation pipeline integrating metric computation, RAGAS scoring, and reporting |
| 05 | [05_agent_trajectory_evaluation](05_agent_trajectory_evaluation.ipynb) | Grading the *steps* an agent took: tool choice, ordering, redundant calls, recovery after failure |

### A note on notebook 05

Notebooks 01-04 evaluate **outputs**. Every RAGAS metric takes
`(question, contexts, answer, ground_truth)` and scores the *result*. For a RAG
chain that is enough - a chain retrieves once and generates once, so it has no
interesting behaviour to grade.

For an **agent** it is badly insufficient, because an agent chooses what to do:
which tool, in what order, when to stop, how to react when a call fails. An agent
that reaches the right answer after eleven redundant searches, two timeouts and a
lucky guess is not a working agent - and output evaluation scores it as a success.

Notebook 05 builds a small instrumented tool-using agent, records its
trajectories, and grades them two ways: **deterministic metrics** (step count,
redundant calls, tool error rate, recovery rate, completion, tool-choice
accuracy) that are free and exact and belong in CI, and an **LLM judge with a
named rubric** for the qualitative dimensions code cannot decide. It closes with
two trajectories that produce the identical correct answer and score identically
under every output metric - and very differently under process metrics. Run it
alongside RAGAS, not instead of it.

It uses Groq `qwen/qwen3.8-27b` (paced for the ~8000 tokens/minute free tier,
with a local Ollama fallback) and contains no skip branches.

## Prerequisites

- LangChain module [10_basic_rag](../../01_langchain/10_basic_rag/README.md) - you need a pipeline before you can score one
- Module 01 ([Hybrid Search](../01_hybrid_search/README.md)) - the retriever these pipelines build on
- Modules 01-09 - any of them can be the system under test

## When to use this technique

- Benchmarking RAG systems before production deployment
- Comparing retrieval strategies, embedding models, or generator configurations
- Establishing quality baselines and tracking regression over pipeline iterations
- Combining automated metrics with human judgment for comprehensive quality assessment
