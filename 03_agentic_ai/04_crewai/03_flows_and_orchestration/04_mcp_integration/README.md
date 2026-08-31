# 04 — MCP Integration

## What is MCP, and why does it matter?

**MCP (Model Context Protocol)** is an open standard for exposing tools
(and other context) to AI agents over a stable, well-defined interface.
Instead of writing custom integration code every time you want an agent to
use a new tool, you point it at an MCP server and it automatically
discovers what that server offers. This matters because it decouples
"who built the tool" from "who built the agent" — you can plug in tools
from anywhere that speaks MCP without custom glue code per tool.

## The three primitives

Most tutorials stop at tools. MCP actually defines **three** primitives,
and the difference between them is *who decides when they're used*:

| Primitive | Controlled by | What it is | Client API |
|---|---|---|---|
| **Tools** | the **model** | Verbs with side effects. The LLM decides to call them. | `list_tools()` / `call_tool()` |
| **Resources** | the **application** | Read-only data addressed by a URI, like files. *Your code* decides what to read and put in the prompt. | `list_resources()` / `read_resource()` |
| **Prompts** | the **user** | Named, argument-taking prompt templates that live on the server. Typically shown to a human as a menu / slash commands. | `list_prompts()` / `get_prompt()` |

Choosing correctly is the real skill:

- If you're writing a tool called `get_config()` that takes no arguments
  and just returns text, that should have been a **resource**. Resources
  are cheaper, deterministic, and the model can't "forget" to fetch them.
- If you're pasting the same carefully-worded f-string into three client
  repos, that should have been a server **prompt** — fix the wording once
  on the server and every client picks it up on its next handshake.
- **Tools** are for genuinely model-driven decisions and side effects:
  anything that depends on an argument the app doesn't know in advance.

> **Important CrewAI detail:** `crewai_tools.MCPServerAdapter` surfaces
> **only tools**, because tools are the only primitive a CrewAI `Agent`
> can invoke on its own. To reach resources and prompts you drop down to
> the official `mcp` SDK's `ClientSession` — that's the layer where
> `read_resource()` and `get_prompt()` live. `mcp_full_primitives.py`
> shows both connections side by side.

## Transports

MCP supports three transports (three ways a client and server can talk):

- **stdio** — the client launches the server as a local subprocess and
  talks to it over its input/output streams. No network involved.
- **SSE (Server-Sent Events)** — the server listens on an HTTP port; used
  for older/simpler network deployments.
- **Streamable HTTP** — MCP's newer, recommended network transport; a
  single HTTP endpoint supporting both request/response and streaming.

Transport and primitive are independent axes: any transport can carry any
primitive. The files here use stdio for the primitive demos to keep the
plumbing out of the way.

## Files in this module

| File | What it teaches |
|---|---|
| `mcp_stdio_server.py` | A real local MCP server (word-count + text-reverse **tools**), run over stdio. |
| `mcp_agent_crew.py` | Connects a CrewAI `Agent` to that stdio server and lets it use the tools inside a real crew run. |
| `mcp_sse_server.py` | The same idea over SSE (network transport), listening on `http://127.0.0.1:8765/sse`. |
| `mcp_http_server.py` | The same idea over Streamable HTTP, listening on `http://127.0.0.1:8766/mcp`. |
| `mcp_http_and_sse_client.py` | Launches both network servers as background processes and connects to each as a real client. |
| `mcp_resources.py` | **RESOURCES**: a server exposing read-only URI-addressed context (static + templated), and a client that lists and reads it. |
| `mcp_prompts.py` | **PROMPTS**: a server shipping reusable prompt templates, and a client that lists, fills, and sends one to a real LLM. |
| `mcp_full_primitives.py` | **All three at once**: one support-desk server with tools + resources + prompts, consumed by a real CrewAI crew. |
| `mcp_authentication.py` | **AUTH**: a token-gated server, a client presenting credentials, scope checks, and the rejection paths for missing/wrong credentials. |
| `main.py` | Runs all six sections in sequence. |

## Walkthrough

1. **`mcp_stdio_server.py`** — Uses the `mcp` SDK's `FastMCP` helper.
   Every function decorated with `@mcp.tool()` automatically becomes a
   tool that a connecting client can discover and call. This file is
   meant to be *launched by* a client, not run and left alone in a
   terminal (running it directly will just sit waiting for stdin input).

2. **`mcp_agent_crew.py`** — `StdioServerParameters` describes how to
   launch the server (which Python interpreter, which script).
   `MCPServerAdapter` starts that process, connects to it, and returns
   CrewAI-compatible tool objects — which are then passed straight into
   `Agent(tools=mcp_tools)` exactly like any other tool.

3. **`mcp_sse_server.py`** / **`mcp_http_server.py`** — Same tool-serving
   idea, but bound to a real localhost port instead of stdio, showing how
   MCP servers can run as long-lived network services.

4. **`mcp_http_and_sse_client.py`** — Starts each network server as a
   background subprocess, waits briefly for it to be ready, connects with
   `MCPServerAdapter({"url": ...})` (note: a dict, not
   `StdioServerParameters`), calls a tool directly, then shuts the server
   down.

5. **`mcp_resources.py`** — A "company handbook" server exposing **zero
   tools** and three resources, to make the separation obvious:
   - a *static* resource at a fixed URI (`course://handbook/index`)
   - two *resource templates* whose URIs contain a `{placeholder}`
     (`course://handbook/policies/{topic}`,
     `course://students/{student_id}`), so one handler serves a whole
     family of addresses
   The client calls `list_resources()`, `list_resource_templates()` and
   `read_resource(uri)`, then assembles a context block from what it
   read — demonstrating that *the app*, not the model, chose the context.

6. **`mcp_prompts.py`** — An incident-management server offering two
   prompt templates: a simple one that returns a string (shorthand for a
   single user message), and a structured one that returns a list of
   `base.AssistantMessage` / `base.UserMessage` objects. The client lists
   them (function parameters become the prompt's declared arguments,
   the docstring becomes its description), fetches one with arguments
   filled in, converts the returned MCP messages into the ordinary
   `[{"role", "content"}]` shape every LLM API accepts, and sends it.
   The structured template inlines a server-side runbook the client
   doesn't have — the concrete case for server-owned prompts.

7. **`mcp_full_primitives.py`** — A customer-support server carrying all
   three primitives, and a crew that uses each for its proper job:
   - **resources** → fetch the refund policy and the customer record up
     front, as trusted read-only context spliced into the `Task`
   - **prompt** → fetch the support team's house-style reply template
     rather than inventing wording client-side
   - **tool** → let the agent call `lookup_order_status` itself, whenever
     it decides it needs live data
   It opens the server twice on purpose: a raw `ClientSession` for the
   resources and prompt, and an `MCPServerAdapter` for the tools that go
   into `Agent(tools=...)`.

8. **`mcp_authentication.py`** — every other file here assumed the
   connection was trusted. This one puts a lock on it, and separates the
   two questions beginners routinely merge:

   | Question | Where it is checked | Carrier |
   |---|---|---|
   | *May this client talk to me at all?* (authentication) | once, when the connection opens | the subprocess **environment** over stdio; an `Authorization: Bearer` **header** over HTTP |
   | *May this caller run **this** tool?* (authorisation) | on every tool call | a **scope** the server looked up from the token |

   The server maps a bearer token to an identity plus a scope set;
   `get_order` needs `orders:read`, `refund_order` needs the stronger
   `orders:refund`. The client half opens four connections and prints
   what happens: a full-scope token (everything works), a read-only
   token (reads fine, **403** on the refund), a wrong token, and no
   token at all — the last two producing *identical* refusals on
   purpose, so an attacker learns nothing from the difference.

   Two details worth internalising:
   - The credential travels on the **transport**, never as a tool
     argument. A token in a tool argument is a token in the model's
     context window, in your traces, and in your logs.
   - The read-only client can still *see* `refund_order` in
     `list_tools()`. Hiding a tool is not protecting it — enforcement
     has to be server-side, because the model cannot be trusted to
     police itself.

   MCP's specified authorization profile is OAuth 2.1 over the HTTP
   transports, which needs a real identity provider to demonstrate. What
   that machinery ultimately produces is exactly the hand-rolled thing
   here: a bearer token the server validates and maps to scopes. The
   hard-coded plaintext token table is a teaching shortcut — real tokens
   live in a secret manager, are stored hashed, and expire.

9. **`main.py`** — runs all six sections in order, pausing between the
   LLM-hitting ones to stay under the Groq free tier's token-per-minute
   budget.

## Self-hosting server files

`mcp_resources.py`, `mcp_prompts.py` and `mcp_full_primitives.py` are each
*both* a server and a client in one file:

```bash
python mcp_resources.py            # acts as the CLIENT (and spawns the server)
python mcp_resources.py --server   # becomes the SERVER, blocking on stdio
```

You'd rarely type the `--server` form yourself — the client half launches
it for you. It's there so the demo stays in a single readable file.

## How to run it

```bash
python mcp_agent_crew.py            # tools: stdio transport, agent + real crew
python mcp_http_and_sse_client.py   # tools: SSE + Streamable HTTP transports
python mcp_resources.py             # resources
python mcp_prompts.py               # prompts
python mcp_full_primitives.py       # tools + resources + prompts, one crew
python main.py                      # everything, in sequence
```

`mcp_stdio_server.py`, `mcp_sse_server.py`, and `mcp_http_server.py` are
**servers** — they're launched automatically by the client files above, so
you don't normally run them directly.

Uses your Groq API key from `03_agentic_ai/.env` (`GROQ_API_KEY`), with a
local Ollama fallback. No OpenAI is used anywhere in this course.
