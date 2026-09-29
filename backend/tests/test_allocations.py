from __future__ import annotations


def _admin_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    return login.json()["access_token"]


def test_create_application(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/applications",
        json={"preferred_room_type": "DOUBLE"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_list_applications(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/applications",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_review_application(client) -> None:
    token = _admin_token(client)
    apps = client.get(
        "/api/v1/applications",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    pending = [a for a in apps if a["status"] == "PENDING"]
    if not pending:
        return
    app_id = pending[0]["id"]
    response = client.put(
        f"/api/v1/applications/{app_id}/review",
        json={"status": "APPROVED", "remarks": "Approved for allocation"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


def test_allocate_bed(client) -> None:
    token = _admin_token(client)
    apps = client.get(
        "/api/v1/applications",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    approved = [a for a in apps if a["status"] == "APPROVED"]
    if not approved:
        return
    app = approved[0]
    response = client.post(
        "/api/v1/allocations",
        json={
            "student_id": app["student_id"],
            "hostel_id": 1,
            "room_id": 1,
            "bed_id": 1,
            "application_id": app["id"],
            "allocation_date": "2024-01-15",
            "check_in_date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "ACTIVE"


def test_duplicate_allocation_prevented(client) -> None:
    token = _admin_token(client)
    allocs = client.get(
        "/api/v1/allocations",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    active = [a for a in allocs if a["status"] == "ACTIVE"]
    if not active:
        return
    alloc = active[0]
    response = client.post(
        "/api/v1/allocations",
        json={
            "student_id": alloc["student_id"],
            "hostel_id": 1,
            "room_id": 2,
            "bed_id": 3,
            "allocation_date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


def test_checkout(client) -> None:
    token = _admin_token(client)
    allocs = client.get(
        "/api/v1/allocations",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    active = [a for a in allocs if a["status"] == "ACTIVE"]
    if not active:
        return
    alloc = active[0]
    response = client.post(
        f"/api/v1/allocations/{alloc['id']}/checkout",
        json={"check_out_date": "2024-06-15"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "CHECKED_OUT"
