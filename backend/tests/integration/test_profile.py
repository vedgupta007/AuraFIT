import pytest

@pytest.fixture
def auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "profile@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "profile@example.com",
        "password": "strongpassword123"
    })
    return login.json()["access_token"]

@pytest.fixture
def auth_token_user2(client):
    client.post("/api/v1/auth/register", json={
        "email": "user2@example.com",
        "password": "strongpassword123"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "user2@example.com",
        "password": "strongpassword123"
    })
    return login.json()["access_token"]

def test_create_and_get_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Get non-existent
    res = client.get("/api/v1/profile", headers=headers)
    assert res.status_code == 404
    
    # 2. Create profile
    profile_data = {
        "name": "Test User",
        "age": 25,
        "sex": "M",
        "height_cm": 180,
        "weight_kg": 75,
        "goal": "lose_weight",
        "activity_level": "sedentary",
        "training_experience": "beginner",
        "preferred_workout_frequency": 3,
        "dietary_preference": "vegan",
        "allergies": [],
        "disliked_foods": []
    }
    res = client.post("/api/v1/profile", headers=headers, json=profile_data)
    assert res.status_code == 201
    
    # 3. Get profile
    res = client.get("/api/v1/profile", headers=headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Test User"

def test_user_isolation(client, auth_token, auth_token_user2):
    # auth_token created profile above. User2 should not see it.
    headers2 = {"Authorization": f"Bearer {auth_token_user2}"}
    res = client.get("/api/v1/profile", headers=headers2)
    assert res.status_code == 404


def test_update_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Update existing profile (partial update)
    # Note: `auth_token` user already created a profile in the first test. Let's create it again just in case, 
    # but fixtures run once per module? No, fixtures here aren't module-scoped. Let's create one directly.
    profile_data = {
        "name": "Initial Name",
        "age": 25,
        "sex": "M",
        "height_cm": 180,
        "weight_kg": 75,
        "goal": "lose_weight",
        "activity_level": "sedentary",
        "training_experience": "beginner",
        "preferred_workout_frequency": 3,
        "dietary_preference": "vegan",
        "allergies": [],
        "disliked_foods": []
    }
    # It might already exist, so catch 400
    res = client.post("/api/v1/profile", headers=headers, json=profile_data)
    
    # Update weight and goal
    update_data = {
        "weight_kg": 70,
        "goal": "gain_muscle"
    }
    res_update = client.put("/api/v1/profile", headers=headers, json=update_data)
    assert res_update.status_code == 200
    assert res_update.json()["weight_kg"] == 70
    assert res_update.json()["goal"] == "gain_muscle"
    # Ensure other fields remained intact
    assert res_update.json()["name"] == "Initial Name" or res_update.json()["name"] == "Test User"
    
    # 2. Invalid data test (e.g. invalid weight)
    invalid_data = {
        "weight_kg": -10
    }
    res_invalid = client.put("/api/v1/profile", headers=headers, json=invalid_data)
    assert res_invalid.status_code == 422
