# AI Agent Tools

**Production AI agent infrastructure** — MCP-driven tools, LangGraph workflows, CrewAI agents, FastAPI backends, and secure automation with typed schemas, guardrails, and controlled execution.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?style=flat&logo=fastapi)]()
[![LangGraph](https://img.shields.io/badge/LangGraph-workflows-purple?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)]()

---

## What's in here

| Module | What it does |
|---|---|
| `mcp-tools/` | MCP server tools for browser inspection, API calls, file processing |
| `agents/` | LangGraph and CrewAI agent implementations with guardrails |
| `api/` | FastAPI backends for agent orchestration and tool serving |
| `workflows/` | Production workflow definitions with polling, webhooks, and cron |
| `schemas/` | Zod and Pydantic typed schemas for all agent inputs and outputs |
| `utils/` | Retry logic, rate limiting, state management, observability |

---

## Architecture

```
Agent layer      LangGraph · CrewAI · LiteLLM multi-model routing
Tool layer       MCP tools · Playwright MCP · Browser inspection · File processing
API layer        FastAPI · REST endpoints · Streaming responses
Security         OAuth 2.0 · JWT · HMAC-SHA256 · Input validation
Reliability      Typed schemas · Guardrails · Retry logic · Idempotency
Orchestration    Webhooks · Polling · Cron jobs · Event-driven execution
```

---

## Key design principles

- **Typed inputs and outputs** — every agent tool uses Pydantic/Zod schemas
- **Controlled execution** — guardrails prevent runaway or brittle behavior
- **Retrieval checks** — agents verify context before acting
- **Predictable, not brittle** — systems behave consistently under load

---

## Quick start

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

---

## Example: MCP browser tool

```python
from mcp import Tool, ToolResult
from playwright.async_api import async_playwright

class BrowserInspectTool(Tool):
    name = "browser_inspect"
    description = "Inspect a page and return structured content"

    async def run(self, url: str) -> ToolResult:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")
            content = await page.content()
            title = await page.title()
            await browser.close()
            return ToolResult(data={"title": title, "content": content[:5000]})
```

---

## Example: LangGraph workflow

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class WorkflowState(TypedDict):
    input: str
    tool_result: str
    final_output: str

def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("inspect", inspect_node)
    graph.add_node("process", process_node)
    graph.add_node("output", output_node)
    graph.add_edge("inspect", "process")
    graph.add_edge("process", "output")
    graph.set_entry_point("inspect")
    return graph.compile()
```

---

## Built by

> [Cerison Brown](https://github.com/CerisonAutomation) — Automation Engineer specialising in AI workflow engineering, MCP agent tooling, and secure production automation systems.
