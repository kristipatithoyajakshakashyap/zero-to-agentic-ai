# 05 Production Security

> **MLCourse - Agentic AI - Production Security**

This sub-track teaches the security, guardrail, caching, and privacy
patterns every production agent needs. It is conceptual and practical --
each module shows the core technique with runnable, deterministic examples
that do **not** require an API key or a cloud provider.

> Note: this path keeps authentication/authorization out of scope by design.
> It focuses on the concepts and how to use them, not a full-stack app.

## Modules

1. [`01_prompt_injection`](01_prompt_injection/) - attack taxonomy, why
   simple mitigations fail, and a working injection detector
2. [`02_guardrail_frameworks`](02_guardrail_frameworks/) - layered input /
   output / action guardrails that fail closed (Pydantic, refusal, grounding)
3. [`03_caching_strategies`](03_caching_strategies/) - exact-match, semantic,
   and TTL caching with cache safety, poisoning, and cache-busting
4. [`04_privacy_and_data`](04_privacy_and_data/) - PII detection / redaction,
   data minimization, and local-first privacy
5. [`05_security_evaluation`](05_security_evaluation/) - automated red-team
   harness measuring recall, precision, and regression coverage

## Learning path

Start at `01_prompt_injection` to understand the threat, then build the
deterministic defenses in `02_guardrail_frameworks`. Add caching in
`03_caching_strategies` (guard first, then cache), protect PII in
`04_privacy_and_data`, and finally measure everything with the harness in
`05_security_evaluation`.

## Companion modules

- Guardrail RAG: `03_rag_advanced/08_vectorless_rag/03_guardrails.ipynb`
- Semantic caching (RAG layer): `03_rag_advanced/07_cache_rag/`
- Observability: `04_crewai/04_production/02_observability/`
- Tool access control / MCP: `04_crewai/03_flows_and_orchestration/04_mcp_integration/`
