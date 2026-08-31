# Module 03 - Caching Strategies

> **MLCourse - Agentic AI - Production Security - Caching Strategies**

Caching cuts cost, latency, and provider load for LLM agents. But caching
has security implications: what you cache, where, and who can read it all
matter. This module covers exact-match, semantic, and TTL caching with a
focus on cache keys, invalidation, poisoning, and cache safety.

## What you'll learn

- Why cache LLM calls (cost, latency, load)
- Exact-match caching and composite cache keys
- Semantic caching using embeddings and similarity
- Time-to-live (TTL) and invalidation strategies
- What is safe to cache vs. what must never be cached
- Cache poisoning and cache-busting on sensitive operations
- Composing caching with guardrails (guard first, then cache)
- Caching **tool** results: keys from name + arguments, per-tool TTL, and
  why side-effecting tools must never be cached

## Key concepts

- **Cache key**: must capture every input that changes the answer
- **Semantic cache**: reuse answers for similar queries via embedding
- **TTL**: expire stale entries automatically
- **Cache poisoning**: unsafe response cached and served to all users
- **Never cache**: secrets, PII, per-user private data, unsafe responses

## Contents

1. `01_caching_strategies.ipynb` - exact-match, semantic, and TTL caches,
   cache safety checklist, poisoning + cache-busting, guarded cache pipeline
2. `02_tool_result_caching.ipynb` - caching **tool calls**, not LLM calls:
   keys from tool name + arguments, the pure/read-only/per-user/side-effecting
   classification, per-tool TTL policy, and why write tools must never be
   cached

After this module, continue to `04_privacy_handling` to see how PII is
detected and redacted so it never reaches models, logs, or caches.
