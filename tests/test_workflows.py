"""Tests for workflow registry and dispatch."""
import pytest
from fastapi.testclient import TestClient
from api.main import app, WORKFLOW_REGISTRY

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_lists_workflows():
    response = client.get("/health")
    workflows = response.json()["workflows"]
    assert "guesty.sync_reservations" in workflows
    assert "agent.summarise_text" in workflows


def test_list_workflows_endpoint():
    response = client.get("/workflows")
    assert response.status_code == 200
    assert "guesty.sync_reservations" in response.json()["workflows"]


def test_unknown_workflow_returns_404():
    response = client.post("/workflows/run", json={
        "workflow_id": "does.not.exist",
        "input_data": {},
    })
    assert response.status_code == 404


def test_all_registered_workflows_are_callable():
    for wf_id, handler in WORKFLOW_REGISTRY.items():
        assert callable(handler), f"{wf_id} handler is not callable"
