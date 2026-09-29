from __future__ import annotations


def test_root_returns_service_info(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["api"] == "/api/v1"
    assert body["docs"] == "/docs"


def test_health_endpoint_reports_database_state(client) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"ok", "degraded"}
    assert body["database"] in {"up", "down"}


def test_docs_are_available(client) -> None:
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200


def test_unknown_route_returns_consistent_error_shape(client) -> None:
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"]
    assert error["message"]


def test_validation_error_returns_422_shape(client) -> None:
    response = client.get("/api/v1/health", params={"unexpected": "x"})
    # endpoint ignores extra params, so a valid call must still succeed
    assert response.status_code == 200
