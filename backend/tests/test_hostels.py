from __future__ import annotations


def _admin_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    return login.json()["access_token"]


def test_create_hostel(client) -> None:
    import uuid
    token = _admin_token(client)
    code = f"TH-{uuid.uuid4().hex[:6].upper()}"
    response = client.post(
        "/api/v1/hostels",
        json={"name": "Test Hostel", "code": code, "address": "123 Test St"},
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 409:
        return
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Test Hostel"
    assert body["code"] == code


def test_list_hostels(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/hostels",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_hostel(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/hostels/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_hostel(client) -> None:
    token = _admin_token(client)
    response = client.put(
        "/api/v1/hostels/1",
        json={"name": "Updated Hostel"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hostel"


def test_delete_hostel(client) -> None:
    token = _admin_token(client)
    create = client.post(
        "/api/v1/hostels",
        json={"name": "To Delete", "code": "DEL1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    hostel_id = create.json()["id"]
    response = client.delete(
        f"/api/v1/hostels/{hostel_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204


def test_hostel_requires_auth(client) -> None:
    response = client.get("/api/v1/hostels")
    assert response.status_code == 401


def test_hostel_requires_admin_role(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/hostels",
        json={"name": "Test", "code": "T1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
