from __future__ import annotations


def _admin_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    return login.json()["access_token"]


def _staff_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "staff", "password": "Staff@123456"},
    )
    return login.json()["access_token"]


def test_mark_attendance(client) -> None:
    import uuid
    token = _staff_token(client)
    day = int(uuid.uuid4().hex[:2], 16) % 28 + 1
    date = f"2024-03-{day:02d}"
    response = client.post(
        "/api/v1/attendance",
        json={
            "student_id": 1,
            "attendance_date": date,
            "status": "PRESENT",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_duplicate_attendance_prevented(client) -> None:
    import uuid
    token = _staff_token(client)
    day = int(uuid.uuid4().hex[:2], 16) % 28 + 1
    date = f"2024-04-{day:02d}"
    client.post(
        "/api/v1/attendance",
        json={
            "student_id": 1,
            "attendance_date": date,
            "status": "PRESENT",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.post(
        "/api/v1/attendance",
        json={
            "student_id": 1,
            "attendance_date": date,
            "status": "ABSENT",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


def test_create_leave_request(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/leaves",
        json={
            "start_date": "2024-03-01",
            "end_date": "2024-03-05",
            "reason": "Family emergency",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_leave_date_validation(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/leaves",
        json={
            "start_date": "2024-03-10",
            "end_date": "2024-03-05",
            "reason": "Invalid dates",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_review_leave(client) -> None:
    token = _admin_token(client)
    leaves = client.get(
        "/api/v1/leaves",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    pending = [l for l in leaves if l["status"] == "PENDING"]
    if not pending:
        return
    leave_id = pending[0]["id"]
    response = client.put(
        f"/api/v1/leaves/{leave_id}/review",
        json={"status": "APPROVED", "remarks": "Approved"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


def test_create_complaint(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/complaints",
        json={"title": "No hot water", "description": "No hot water in bathroom for 3 days"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_create_maintenance_request(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.post(
        "/api/v1/maintenance",
        json={"room_id": 1, "title": "Broken window", "description": "Window is broken"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_update_complaint_status(client) -> None:
    token = _admin_token(client)
    complaints = client.get(
        "/api/v1/complaints",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    if complaints:
        comp_id = complaints[0]["id"]
        response = client.put(
            f"/api/v1/complaints/{comp_id}",
            json={"status": "IN_PROGRESS"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "IN_PROGRESS"
