import pytest

@pytest.fixture
def auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "foods@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "foods@example.com",
        "password": "strongpassword123"
    })
    return login.json()["access_token"]

def test_get_foods_list(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert isinstance(data["items"], list)

def test_get_foods_search(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods?search=Apple", headers=headers)
    assert res.status_code == 200
    items = res.json()["items"]
    # If seed is loaded, we should find Apple
    if len(items) > 0:
        assert "Apple" in items[0]["name"]

def test_get_foods_filters(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods?is_vegetarian=true&category=Fruits", headers=headers)
    assert res.status_code == 200
    for item in res.json()["items"]:
        assert item["is_vegetarian"] == True
        assert item["category"] == "Fruits"

def test_get_food_detail(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods", headers=headers)
    items = res.json()["items"]
    if len(items) > 0:
        food_id = items[0]["id"]
        res_detail = client.get(f"/api/v1/foods/{food_id}", headers=headers)
        assert res_detail.status_code == 200
        assert res_detail.json()["id"] == food_id

def test_get_food_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods/60c72b2f9b1d8b1f4c8b4567", headers=headers)
    assert res.status_code == 404

def test_invalid_object_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/v1/foods/invalid_id_format", headers=headers)
    assert res.status_code == 400
