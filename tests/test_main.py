"""Testes unitários da API.

Rodam no step de `test` do pipeline (pytest). Cobrem o health check e a
lógica do endpoint /sum.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_responds():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_sum_adds_two_numbers():
    response = client.get("/sum", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_sum_handles_negatives():
    response = client.get("/sum", params={"a": -4, "b": 1})
    assert response.json() == {"result": -3}
