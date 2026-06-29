"""FastAPI backend for agent orchestration and tool serving."""

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import logging

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


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/workflows/run", response_model=WorkflowResult)
async def run_workflow(request: WorkflowRequest):
    """Run a named workflow with typed input."""
    try:
        logger.info(f"Running workflow: {request.workflow_id}")
        # Workflow registry dispatches to correct handler
        result = await dispatch_workflow(request.workflow_id, request.input_data)
        return WorkflowResult(
            workflow_id=request.workflow_id,
            status="completed",
            result=result,
        )
    except Exception as e:
        logger.error(f"Workflow failed: {request.workflow_id} - {e}")
        return WorkflowResult(
            workflow_id=request.workflow_id,
            status="failed",
            error=str(e),
        )


async def dispatch_workflow(workflow_id: str, input_data: dict) -> dict:
    """Dispatch to registered workflow handlers."""
    # Registry pattern — extend with your own workflows
    registry = {}
    handler = registry.get(workflow_id)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return await handler(input_data)
