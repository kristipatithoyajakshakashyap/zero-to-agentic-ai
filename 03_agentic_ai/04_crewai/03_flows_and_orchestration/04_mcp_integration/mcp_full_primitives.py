"""ALL THREE MCP PRIMITIVES AT ONCE: one server exposing tools + resources +
prompts, consumed by a real CrewAI crew.

BEGINNER NOTES
--------------
mcp_agent_crew.py showed TOOLS. mcp_resources.py showed RESOURCES.
mcp_prompts.py showed PROMPTS. Real MCP servers ship all three together, and
a well-built agent app uses each one for the job it is designed for:

    PRIMITIVE   CONTROLLED BY   ROLE IN THIS FILE
    ---------   -------------   ----------------------------------------
    resource    the app         Fetch the refund policy + the customer's
                                record, and paste them into the task as
                                trusted, read-only context.
    prompt      the user        Fetch the support team's own reply
                                template from the server instead of
                                inventing wording client-side.
    tool        the model       Let the agent look up live order status
                                itself, whenever it decides it needs to.

Read that table twice — choosing the right primitive is the actual skill.
A beginner's instinct is to make everything a tool. Don't: context the app
already knows it needs should be a resource (cheaper, deterministic, no
chance the model forgets to fetch it), and wording should be a prompt.
Tools are for genuinely model-driven decisions and side effects.

TWO CONNECTIONS, ONE SERVER SCRIPT
----------------------------------
CrewAI's `MCPServerAdapter` surfaces only tools, since that's the only
primitive an `Agent` can invoke on its own. So we open the server twice:

  * a raw `mcp.ClientSession`  -> for resources and prompts (app/user side)
  * an `MCPServerAdapter`      -> for tools handed to `Agent(tools=...)`

Each opens its own stdio subprocess of this same file in --server mode.
That's normal: MCP servers are cheap and stateless here.

LLM provider: Groq is primary (GROQ_API_KEY from 03_agentic_ai/.env), with a
local Ollama server as the only fallback. OpenAI is never used in this course.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base  # module-level so FastMCP can resolve
                                             # the `list[base.Message]` annotation below

if TYPE_CHECKING:  # `crewai` is imported lazily, see note in get_llm()
    from crewai import LLM

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"
THIS_FILE = Path(__file__).resolve()


def _load_track_env() -> None:
    track_dir = Path(__file__).resolve().parent
    while track_dir.name != "03_agentic_ai" and track_dir.parent != track_dir:
        track_dir = track_dir.parent
    load_dotenv(dotenv_path=track_dir / ".env")


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> LLM:
    """Resolve an LLM: Groq first, local Ollama fallback. No OpenAI, ever."""
    # Imported here rather than at module top because this same file also runs
    # as the MCP *server* subprocess, which has no business loading CrewAI.
    from crewai import LLM

    _load_track_env()
    groq_model = model or os.getenv("CREWAI_GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        try:
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return LLM(model=f"groq/{groq_model}", api_key=api_key, temperature=temperature, **kwargs)
        except requests.RequestException:
            pass

    try:
        if requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3).status_code == 200:
            return LLM(model=f"ollama/{DEFAULT_OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL, temperature=temperature, **kwargs)
    except requests.RequestException:
        pass

    raise RuntimeError(
        "No LLM provider available. Set GROQ_API_KEY in 03_agentic_ai/.env, "
        f"or run a local Ollama server at {OLLAMA_BASE_URL} with `ollama pull {DEFAULT_OLLAMA_MODEL}`."
    )


# ---------------------------------------------------------------------------
# THE SERVER SIDE — a small "customer support" server offering all three
# ---------------------------------------------------------------------------
ORDERS = {
    "A-1001": {"status": "delivered", "delivered_on": "2026-08-19", "total_usd": 129.00},
    "A-1002": {"status": "in_transit", "eta": "2026-08-30", "total_usd": 54.50},
}

CUSTOMERS = {
    "c-77": {"name": "Ada Lovelace", "tier": "gold", "orders": ["A-1001", "A-1002"]},
}

REFUND_POLICY = (
    "Refunds are issued within 14 days of DELIVERY. Gold-tier customers get a "
    "30-day window and free return shipping. Items must be unopened."
)


def build_server() -> FastMCP:
    """One FastMCP server carrying tools, resources AND prompts."""
    mcp = FastMCP("course-support-desk", log_level="ERROR")

    # ---- TOOL (model-controlled) --------------------------------------
    # The agent calls this when *it* decides it needs live order data. Note
    # it takes an argument the app doesn't know in advance — that argument
    # dependence is the giveaway that this belongs as a tool, not a resource.
    @mcp.tool()
    def lookup_order_status(order_id: str) -> str:
        """Look up the live status of one order by its ID (e.g. 'A-1002')."""
        order = ORDERS.get(order_id)
        if order is None:
            return f"No order found with id {order_id}."
        return json.dumps({"order_id": order_id, **order})

    # ---- RESOURCES (app-controlled) -----------------------------------
    # Read-only context addressed by URI. The app fetches these up front
    # because it already knows the conversation will need them.
    @mcp.resource("support://policies/refund", mime_type="text/plain")
    def refund_policy() -> str:
        """The current refund policy, verbatim."""
        return REFUND_POLICY

    @mcp.resource("support://customers/{customer_id}", mime_type="application/json")
    def customer_record(customer_id: str) -> str:
        """One customer's record as JSON (name, tier, order ids)."""
        return json.dumps(CUSTOMERS.get(customer_id, {"error": f"unknown customer {customer_id}"}))

    # ---- PROMPT (user-controlled) -------------------------------------
    # The support team's own house style, owned and versioned by the team
    # that owns this server, not copy-pasted into every client app.
    @mcp.prompt()
    def support_reply(customer_name: str, question: str) -> list[base.Message]:
        """The support desk's house-style template for answering a customer."""
        return [
            base.AssistantMessage(
                "House style: warm but brief, no more than 4 sentences, always "
                "state the concrete next step, never promise a refund you have "
                "not verified against the policy."
            ),
            base.UserMessage(
                f"Write a reply to {customer_name}, who asks: {question}"
            ),
        ]

    return mcp


# ---------------------------------------------------------------------------
# THE CLIENT SIDE — step 1: gather resources + prompt over a raw session
# ---------------------------------------------------------------------------
async def _gather_context(customer_id: str, question: str) -> dict[str, str]:
    """Use the raw MCP session for the two primitives CrewAI can't reach.

    Returns a small dict of plain strings that we'll splice into the crew's
    Task description. Nothing here involves the LLM at all — this is your
    application deciding what context the agent gets.
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[str(THIS_FILE), "--server"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Prove all three primitives live on this ONE server.
            tools = await session.list_tools()
            resources = await session.list_resources()
            templates = await session.list_resource_templates()
            prompts = await session.list_prompts()
            print("One server, three primitives:")
            print(f"  tools     : {[t.name for t in tools.tools]}")
            print(f"  resources : {[str(r.uri) for r in resources.resources]}")
            print(f"  templates : {[t.uriTemplate for t in templates.resourceTemplates]}")
            print(f"  prompts   : {[p.name for p in prompts.prompts]}")

            # RESOURCES: the app fetches exactly what it knows it needs.
            policy = (await session.read_resource("support://policies/refund")).contents[0].text
            customer_json = (
                await session.read_resource(f"support://customers/{customer_id}")
            ).contents[0].text
            customer = json.loads(customer_json)

            # PROMPT: the server owns the wording. We flatten the rendered
            # messages into one instruction block that a CrewAI Task can carry.
            rendered = await session.get_prompt(
                "support_reply",
                arguments={"customer_name": customer.get("name", "the customer"), "question": question},
            )
            instructions = "\n".join(
                getattr(m.content, "text", str(m.content)) for m in rendered.messages
            )

            return {
                "policy": policy,
                "customer_json": customer_json,
                "customer_name": customer.get("name", "the customer"),
                "known_orders": ", ".join(customer.get("orders", [])),
                "instructions": instructions,
            }


# ---------------------------------------------------------------------------
# THE CLIENT SIDE — step 2: run a real crew with the server's tools
# ---------------------------------------------------------------------------
def run_support_crew(
    customer_id: str = "c-77",
    question: str = "Can I still return order A-1002? And where is it right now?",
) -> str:
    """Gather resources + prompt, then run a CrewAI crew wired to the tools."""
    from crewai import Agent, Crew, Process, Task
    from crewai_tools import MCPServerAdapter
    from mcp import StdioServerParameters

    ctx = asyncio.run(_gather_context(customer_id, question))

    print("\n--- Context the APP fetched via resources (no LLM involved) ---")
    print(f"policy  : {ctx['policy']}")
    print(f"customer: {ctx['customer_json']}")
    print("\n--- Instructions the SERVER supplied via its prompt template ---")
    print(ctx["instructions"])

    server_params = StdioServerParameters(command=sys.executable, args=[str(THIS_FILE), "--server"])

    # MCPServerAdapter spawns its own copy of the server and returns only the
    # TOOLS as CrewAI-compatible tool objects.
    with MCPServerAdapter(server_params) as mcp_tools:
        print(f"\nTools handed to the agent: {[t.name for t in mcp_tools]}")

        agent = Agent(
            role="Customer Support Specialist",
            goal="Answer the customer correctly using the provided policy and live order data",
            backstory=(
                "You never guess an order's status — you call the lookup_order_status "
                "tool. You never contradict the refund policy you were given."
            ),
            llm=get_llm(),
            tools=mcp_tools,
            verbose=False,
        )

        # The Task description is where all three primitives converge:
        # prompt-derived instructions + resource-derived facts + a nudge to
        # use the tool for anything live.
        task = Task(
            description=(
                f"{ctx['instructions']}\n\n"
                f"REFUND POLICY (authoritative, from the support server):\n{ctx['policy']}\n\n"
                f"CUSTOMER RECORD: {ctx['customer_json']}\n"
                f"Their order ids: {ctx['known_orders']}\n\n"
                "Use the lookup_order_status tool for any order you need live status on. "
                f"The customer's question was: {question}"
            ),
            expected_output="A short support reply in the house style, grounded in the policy and live order status.",
            agent=agent,
        )

        result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
        return str(result)


def demo_full_primitives() -> None:
    """Sync wrapper so main.py can call this like every other section."""
    print(run_support_crew())


if __name__ == "__main__":
    if "--server" in sys.argv:
        # Child process: become the MCP server and block, serving over stdio.
        build_server().run(transport="stdio")
    else:
        print("\n--- Crew answer (tools + resources + prompts combined) ---")
        demo_full_primitives()
