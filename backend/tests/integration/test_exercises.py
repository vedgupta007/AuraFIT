import pytest

@pytest.fixture
def auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "exercises@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "exercises@example.com",
        "password": "strongpassword123"
    })
    return login.json()["access_token"]

def test_get_exercises_list(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/exercises", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert isinstance(data["items"], list)

def test_get_exercises_search(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/exercises?search=Squats", headers=headers)
    assert res.status_code == 200
    items = res.json()["items"]
    if len(items) > 0:
        assert "Squats" in items[0]["name"]

def test_get_exercises_filters(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/exercises?difficulty=Beginner&equipment=Bodyweight", headers=headers)
    assert res.status_code == 200
    for item in res.json()["items"]:
        assert item["difficulty"] == "Beginner"
        assert item["equipment"] == "Bodyweight"

def test_get_exercise_detail(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/exercises", headers=headers)
    items = res.json()["items"]
    if len(items) > 0:
        ex_id = items[0]["id"]
        res_detail = client.get(f"/api/v1/exercises/{ex_id}", headers=headers)
        assert res_detail.status_code == 200
        assert res_detail.json()["id"] == ex_id

def test_get_exercise_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/exercises/60c72b2f9b1d8b1f4c8b4567", headers=headers)
    assert res.status_code == 404
