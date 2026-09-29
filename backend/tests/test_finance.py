from __future__ import annotations


def _admin_token(client) -> str:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123456"},
    )
    return login.json()["access_token"]


def test_create_fee_structure(client) -> None:
    token = _admin_token(client)
    response = client.post(
        "/api/v1/fees",
        json={
            "hostel_id": 1,
            "name": "Test Fee",
            "fee_type": "OTHER",
            "amount": 500,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 500


def test_list_fees(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/fees",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_payment(client) -> None:
    token = _admin_token(client)
    fees = client.get(
        "/api/v1/fees",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    if not fees:
        return
    response = client.post(
        "/api/v1/payments",
        json={
            "student_id": 1,
            "fee_structure_id": fees[0]["id"],
            "amount": fees[0]["amount"],
            "payment_method": "CASH",
            "payment_date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "PAID"


def test_list_payments(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/payments",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_expense(client) -> None:
    token = _admin_token(client)
    response = client.post(
        "/api/v1/expenses",
        json={
            "hostel_id": 1,
            "title": "Electricity Bill",
            "category": "Utilities",
            "amount": 5000,
            "expense_date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 5000


def test_list_expenses(client) -> None:
    token = _admin_token(client)
    response = client.get(
        "/api/v1/expenses",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
