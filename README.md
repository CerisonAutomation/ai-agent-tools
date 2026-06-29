# AI Agent Tools

**AI agent infrastructure** — MCP-driven tools, LangGraph workflows, CrewAI agents, FastAPI backends, and secure production automation with guardrails, typed schemas, and controlled execution.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)]()
[![LangChain](https://img.shields.io/badge/LangChain-0.2-green?style=flat)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen?style=flat)]()
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=flat&logo=githubactions)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)]()

---

## Structure

```
ai-agent-tools/
├── api/
│   ├── main.py                     # FastAPI app — workflow registry + /run endpoint
│   └── workflows/
│       ├── guesty_sync.py          # Fetch + sync Guesty reservations
│       └── summarise_text.py       # LLM text summarisation (OpenRouter/OpenAI)
├── schemas/
│   └── agent-schemas.ts            # TypeScript Zod schemas for agent I/O
├── utils/
│   ├── idempotency.py              # Idempotency key store
│   ├── retry.py                    # Async exponential backoff retry decorator
│   └── rate_limiter.py             # Token-bucket rate limiter
├── tests/
│   ├── test_workflows.py           # Registry, dispatch, 404 handling
│   ├── test_rate_limiter.py        # Token bucket behaviour
│   └── test_retry.py               # Retry decorator — success, partial fail, exhaustion
├── .github/workflows/ci.yml        # GitHub Actions CI — runs on every push
├── requirements.txt
├── Makefile
└── .env.example
```

---

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env
make dev
# API at http://localhost:8002
```

---

## Run tests

```bash
make test
# or
pytest tests/ -v
```

---

## Registered workflows

| Workflow ID | What it does |
|---|---|
| `guesty.sync_reservations` | Fetch reservations from Guesty API for a date window |
| `agent.summarise_text` | Summarise arbitrary text via LLM (OpenRouter / OpenAI) |

Add new workflows by dropping a function in `api/workflows/` and registering in `WORKFLOW_REGISTRY`.

---

## API

```bash
# List registered workflows
curl http://localhost:8002/workflows

# Run a workflow
curl -X POST http://localhost:8002/workflows/run \
  -H 'content-type: application/json' \
  -d '{"workflow_id": "agent.summarise_text", "input_data": {"text": "FastAPI is a modern Python web framework.", "max_words": 20}}'
```

---

## Built by

> [Cerison Brown](https://github.com/CerisonAutomation) — Automation Engineer specialising in AI agent infrastructure, multi-model orchestration, and production Python workflow systems.
