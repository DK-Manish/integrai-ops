import pytest
from httpx import AsyncClient


async def test_register_creates_user(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test.user@example.com", "password": "password123", "full_name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test.user@example.com"
    assert data["role"] == "operator"
    assert "hashed_password" not in data


async def test_register_rejects_duplicate_email(client: AsyncClient) -> None:
    payload = {"email": "dupe@example.com", "password": "password123", "full_name": "Dupe User"}
    first = await client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


async def test_register_rejects_short_password(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "shortpw@example.com", "password": "short", "full_name": "Short PW"},
    )
    assert response.status_code == 422


async def test_login_succeeds_with_correct_credentials(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login.test@example.com", "password": "password123", "full_name": "Login Test"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login.test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in response.cookies


async def test_login_rejects_wrong_password(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpw@example.com", "password": "password123", "full_name": "Wrong PW"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpw@example.com", "password": "incorrect"},
    )
    assert response.status_code == 401


async def test_login_rejects_unknown_email(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "doesnotexist@example.com", "password": "password123"},
    )
    assert response.status_code == 401


async def test_me_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


async def test_me_returns_current_user_with_valid_token(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "me.test@example.com", "password": "password123", "full_name": "Me Test"},
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "me.test@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me.test@example.com"


async def test_refresh_issues_new_access_token(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "refresh.test@example.com", "password": "password123", "full_name": "Refresh Test"},
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "refresh.test@example.com", "password": "password123"},
    )
    original_token = login_response.json()["access_token"]

    refresh_response = await client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 200
    new_token = refresh_response.json()["access_token"]
    assert new_token != original_token


async def test_refresh_without_cookie_is_rejected(client: AsyncClient) -> None:
    response = await client.post("/api/v1/auth/refresh")
    assert response.status_code == 401