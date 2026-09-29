from __future__ import annotations


def _admin_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    return login.json()["access_token"]


def test_create_student(client) -> None:
    import uuid
    token = _admin_token(client)
    suffix = uuid.uuid4().hex[:6]
    response = client.post(
        "/api/v1/students",
        json={
            "username": f"newstudent{suffix}",
            "email": f"newstudent{suffix}@test.com",
            "full_name": "New Student",
            "password": "Test@123456",
            "student_number": f"STU-2024-{suffix.upper()}",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["student_number"] == f"STU-2024-{suffix.upper()}"


def test_list_students(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/students",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/students/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_duplicate_student_number(client) -> None:
    token = _admin_token(client)
    response = client.post(
        "/api/v1/students",
        json={
            "username": "dupstudent",
            "email": "dup@test.com",
            "full_name": "Dup Student",
            "password": "Test@123456",
            "student_number": "STU-2024-001",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


def test_student_me_endpoint(client) -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "student", "password": "Student@123456"},
    )
    token = login.json()["access_token"]
    response = client.get(
        "/api/v1/students/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["student_number"] == "STU-2024-001"
