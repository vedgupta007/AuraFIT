import pytest

def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test_register@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "password": "strongpassword123"
    })
    response = client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 400

def test_invalid_registration(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "not-an-email",
        "password": "short"
    })
    assert response.status_code == 422

def test_login(client):
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "strongpassword123"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_incorrect_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "strongpassword123"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_protected_route_without_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_authenticated_me(client):
    client.post("/api/v1/auth/register", json={
        "email": "me@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "me@example.com",
        "password": "strongpassword123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_login_different_casing(client):
    client.post("/api/v1/auth/register", json={
        "email": "CaseTest@Example.com",
        "password": "strongpassword123"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "casetest@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_leading_trailing_spaces(client):
    client.post("/api/v1/auth/register", json={
        "email": " space@example.com ",
        "password": "strongpassword123"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "space@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_unknown_email(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "unknown@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 404

def test_logout(client):
    register_response = client.post("/api/v1/auth/register", json={
        "email": "logout@example.com",
        "password": "strongpassword123"
    })
    token = register_response.json()["access_token"]
    response = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_refresh_token(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "refresh@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    refresh_cookie = response.cookies.get("refresh_token")
    assert refresh_cookie is not None
    
    refresh_res = client.post("/api/v1/auth/refresh", cookies={"refresh_token": refresh_cookie})
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()
