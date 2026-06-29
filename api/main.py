"""FastAPI backend for agent orchestration and tool serving."""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import logging

from api.workflows.guesty_sync import guesty_sync_reservations
from api.workflows.summarise_text import summarise_text

logger = logging.getLogger(__name__)
app = FastAPI(title="AI Agent Tools API", version="1.0.0")


class WorkflowRequest(BaseModel):
    workflow_id: str
    input_data: dict
    idempotency_key: Optional[str] = None


class WorkflowResult(BaseModel):
    workflow_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None


# Workflow registry — add new workflows here
WORKFLOW_REGISTRY = {
    "guesty.sync_reservations": guesty_sync_reservations,
    "agent.summarise_text":     summarise_text,
}


@app.get("/health")
async def health():
    return {"status": "ok", "workflows": list(WORKFLOW_REGISTRY.keys())}


@app.get("/workflows")
async def list_workflows():
    return {"workflows": list(WORKFLOW_REGISTRY.keys())}


@app.post("/workflows/run", response_model=WorkflowResult)
async def run_workflow(request: WorkflowRequest):
    handler = WORKFLOW_REGISTRY.get(request.workflow_id)
    if not handler:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{request.workflow_id}' not found. Available: {list(WORKFLOW_REGISTRY.keys())}"
        )
    try:
        logger.info(f"Running workflow: {request.workflow_id}")
        result = await handler(request.input_data)
        return WorkflowResult(workflow_id=request.workflow_id, status="completed", result=result)
    except Exception as e:
        logger.error(f"Workflow failed: {request.workflow_id} - {e}")
        return WorkflowResult(workflow_id=request.workflow_id, status="failed", error=str(e))
