# Module 12: Agent Protocols

> **MLCourse - Agentic AI - Agent Patterns**

Every multi-agent pattern earlier in this course — LangGraph subgraphs,
CrewAI crews, MCP tool servers — assumes you control both sides of the
integration. **A2A (Agent2Agent)** is the protocol for when you don't: two
independently built, independently hosted agents, owned by different
parties, connected only by messages.

## What the concept is

A2A gives agents three things a plain function call cannot:

- **Agent Cards** — a discoverable, checkable description of what an agent
  can do, published *before* any connection is made.
- **Tasks** — a unit of delegated work with a real status machine
  (`submitted → working → input-required? → completed/failed`), so work can
  genuinely span multiple turns.
- **Messages** — one turn of a Task's conversation, carrying typed **Parts**.

The one-sentence distinction from MCP: **MCP connects an agent to tools. A2A
connects an agent to another agent.** A tool has no autonomy and no memory; an
agent does — it can decide how to satisfy a request and ask a clarifying
question mid-task, which is exactly what this module's worked example does.

## Why it matters

- It is the protocol for the integration shape this course has not covered:
  crossing an organisational or trust boundary where you cannot see or
  control the other side's implementation.
- It composes with MCP rather than competing with it — a realistic system
  uses MCP for tools it owns and A2A for agents it does not, at the same time.
- Reaching for it when a typed MCP tool call would do is a real, avoidable
  cost: A2A trades a validated schema for a negotiation layer, and that trade
  only pays off when there is something to negotiate.

## Notebooks

| # | Notebook | Focus |
|---|----------|-------|
| 01 | [01_why_agent_protocols](01_why_agent_protocols.ipynb) | Why same-runtime patterns break down; Agent Card, Task, Message |
| 02 | [02_two_local_agents](02_two_local_agents.ipynb) | Two full local agents exchanging real A2A-shaped messages, including a genuine `input-required` negotiation |
| 03 | [03_a2a_vs_mcp](03_a2a_vs_mcp.ipynb) | A2A vs MCP, structurally compared; a worked system needing both; when A2A is the wrong call |

### Walkthrough

**01 — Why agent protocols exist.** Names the property every earlier
multi-agent pattern shared (a common runtime) and the property A2A is for
(no shared code, no shared trust, work that can outlive one request). Builds
the three core objects as plain dataclasses and publishes a worked Agent
Card for a "SkyBooker" flight-booking agent.

**02 — Two local agents.** Implements `SkyBookerAgent` (the callee) and
`TravelerAgent` (the caller) as independent classes that exchange only
`Task`/`Message` objects — no shared Python state, mirroring the constraint a
real HTTP boundary imposes. `SkyBooker` genuinely needs a fare class it
wasn't given, replies with `status=input-required`, and `TravelerAgent`
answers on the same `task_id` — a real multi-turn negotiation, plus the two
honest failure paths (no matching skill; skill matches but the request is
invalid).

**03 — A2A vs MCP.** The structural comparison table, then a trip-planning
system that needs both at once: MCP for tools it owns (weather, currency
conversion), A2A for a partner airline's booking agent it does not control.
Includes the case people get wrong — an external partner's *stateless,
typed* endpoint is still an MCP shape, not an A2A one — and closes with when
reaching for A2A is a real mistake.

## Prerequisites

- [`04_crewai/.../04_mcp_integration`](../../04_crewai/03_flows_and_orchestration/04_mcp_integration/README.md)
  — this module assumes you know MCP's tools/resources/prompts and its
  authentication story, and builds the comparison directly against it.
- [`02_langgraph/06_multi_agent_systems`](../../02_langgraph/06_multi_agent_systems/README.md)
  — useful contrast: multi-agent patterns that *do* share a runtime.

## Providers and keys

**None.** All three notebooks are pure Python — the message shapes, the two
agents, and the comparison logic are all deterministic and local. There are
**no LLM calls and no API key** anywhere in this module; the point is the
protocol's structure, not generation quality.

## Setup

Nothing to install beyond the course's base Python environment (`dataclasses`,
`json`, `uuid` — all standard library).

## Key takeaways

- **MCP connects an agent to tools. A2A connects an agent to another agent.**
  Every structural difference follows from that sentence.
- **Agent Card** = discoverable capability description, checked before
  connecting. **Task** = delegated work with a real status machine. **Message**
  = one turn, carrying typed Parts, tied to a `taskId`.
- `input-required` is what lets a remote agent ask a genuine clarifying
  question mid-task — something a plain function call, or an MCP tool call,
  cannot do.
- A real system typically needs **both protocols**, chosen per integration
  point by asking: is the other side a tool, or a decision-maker?
- A2A is the wrong choice when the interaction is reliably one request and one
  response with a known, typed shape — that is what MCP already solves.
