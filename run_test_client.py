
from app import create_app


app = create_app("testing")

with app.test_client() as client:
    # 1. Register a test user
    register_resp = client.post(
        "/register",
        json={
            "username": "test_client_user",
            "email": "test_client_user@example.com",
            "password": "TestPass123!",
        },
    )

    print("REGISTER:", register_resp.status_code, register_resp.get_json())

    # 2. Log in with the same user
    login_resp = client.post(
        "/login",
        json={
            "username": "test_client_user",
            "password": "TestPass123!",
        },
    )

    login_data = login_resp.get_json() or {}
    print(
        "LOGIN:",
        login_resp.status_code,
        {
            "username": login_data.get("username"),
            "role": login_data.get("role"),
            "token_received": bool(login_data.get("token")),
            "error": login_data.get("error"),
        },
    )
