import pytest
from datetime import datetime, timezone

@pytest.fixture
def auth_client(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "nutri_test@example.com",
        "password": "Password123!"
    })
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def auth_client_2(client):
    # Need a fresh client context for a separate user? Or just register a second user and update headers
    # We can just use the same client but register a new user and swap headers, but to be safe:
    response = client.post("/api/v1/auth/register", json={
        "email": "nutri_test2@example.com",
        "password": "Password123!"
    })
    token = response.json()["access_token"]
    
    # Store token so tests can swap it if they want, but let's just create a new dict for headers
    return token

def test_create_meal(auth_client):
    payload = {
        "meal_type": "breakfast",
        "meal_name": "Oatmeal with Berries",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "1 bowl",
        "calories": 350,
        "protein_grams": 10.5,
        "carbohydrates_grams": 60.0,
        "fat_grams": 5.0,
        "fiber_grams": 8.0,
        "notes": "Very tasty"
    }
    
    response = auth_client.post("/api/v1/nutrition/meals", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["meal_name"] == "Oatmeal with Berries"
    assert data["calories"] == 350
    assert "id" in data
    assert "user_id" in data

def test_create_meal_invalid_data(auth_client):
    payload = {
        "meal_type": "midnight_snack",
        "meal_name": "",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "1 bowl",
        "calories": -100,
        "protein_grams": 10.5,
        "carbohydrates_grams": 60.0,
        "fat_grams": 5.0,
        "fiber_grams": 8.0
    }
    
    response = auth_client.post("/api/v1/nutrition/meals", json=payload)
    assert response.status_code == 422

def test_get_meals(auth_client):
    auth_client.post("/api/v1/nutrition/meals", json={
        "meal_type": "lunch",
        "meal_name": "Chicken Salad",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "1 plate",
        "calories": 400,
        "protein_grams": 30.0,
        "carbohydrates_grams": 10.0,
        "fat_grams": 15.0,
        "fiber_grams": 4.0
    })
    
    response = auth_client.get("/api/v1/nutrition/meals")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(meal["meal_name"] == "Chicken Salad" for meal in data)

def test_idor_protection(auth_client, auth_client_2):
    create_response = auth_client.post("/api/v1/nutrition/meals", json={
        "meal_type": "dinner",
        "meal_name": "Steak",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "8 oz",
        "calories": 600,
        "protein_grams": 50.0,
        "carbohydrates_grams": 0.0,
        "fat_grams": 40.0,
        "fiber_grams": 0.0
    })
    meal_id = create_response.json()["id"]
    
    # Swap headers to user 2
    auth_client.headers = {"Authorization": f"Bearer {auth_client_2}"}
    
    get_response = auth_client.get(f"/api/v1/nutrition/meals/{meal_id}")
    assert get_response.status_code == 404
    
    patch_response = auth_client.patch(f"/api/v1/nutrition/meals/{meal_id}", json={"meal_name": "Stolen Steak"})
    assert patch_response.status_code == 404
    
    delete_response = auth_client.delete(f"/api/v1/nutrition/meals/{meal_id}")
    assert delete_response.status_code == 404

def test_daily_summary(auth_client):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    auth_client.post("/api/v1/nutrition/meals", json={
        "meal_type": "breakfast",
        "meal_name": "Eggs",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "2 eggs",
        "calories": 140,
        "protein_grams": 12.0,
        "carbohydrates_grams": 1.0,
        "fat_grams": 10.0,
        "fiber_grams": 0.0
    })
    
    auth_client.post("/api/v1/nutrition/meals", json={
        "meal_type": "snack",
        "meal_name": "Apple",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "1 medium",
        "calories": 95,
        "protein_grams": 0.5,
        "carbohydrates_grams": 25.0,
        "fat_grams": 0.3,
        "fiber_grams": 4.4
    })
    
    response = auth_client.get(f"/api/v1/nutrition/daily-summary?date={today}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["date"] == today
    assert data["total_calories"] >= 235
    assert data["total_protein"] >= 12.5
    assert data["total_carbohydrates"] >= 26.0
    assert data["meal_count"] >= 2

def test_delete_meal(auth_client):
    create_response = auth_client.post("/api/v1/nutrition/meals", json={
        "meal_type": "snack",
        "meal_name": "To be deleted",
        "consumed_at": datetime.now(timezone.utc).isoformat(),
        "serving_size": "1",
        "calories": 100,
        "protein_grams": 0.0,
        "carbohydrates_grams": 0.0,
        "fat_grams": 0.0,
        "fiber_grams": 0.0
    })
    meal_id = create_response.json()["id"]
    
    delete_response = auth_client.delete(f"/api/v1/nutrition/meals/{meal_id}")
    assert delete_response.status_code == 204
    
    get_response = auth_client.get(f"/api/v1/nutrition/meals/{meal_id}")
    assert get_response.status_code == 404

def test_nutrition_goals(auth_client):
    # Create profile first to ensure goals can be calculated
    profile_payload = {
        "name": "Test User",
        "age": 30,
        "sex": "M",
        "height_cm": 180.0,
        "weight_kg": 80.0,
        "goal": "lose_weight",
        "activity_level": "moderate",
        "training_experience": "intermediate",
        "preferred_workout_frequency": 4,
        "dietary_preference": "non_vegetarian",
        "allergies": [],
        "disliked_foods": []
    }
    auth_client.post("/api/v1/profile", json=profile_payload)
    
    # Check goals calculation
    response = auth_client.get("/api/v1/nutrition/goals")
    assert response.status_code == 200
    data = response.json()
    assert "bmr" in data
    assert "tdee" in data
    assert "daily_calories" in data
    assert "daily_protein" in data
    
    # Verify BMR logic (Mifflin-St Jeor)
    # (10 * 80) + (6.25 * 180) - (5 * 30) + 5 = 800 + 1125 - 150 + 5 = 1780
    assert data["bmr"] == 1780
    
    # Verify TDEE (Moderate = 1.55) -> 1780 * 1.55 = 2759
    assert data["tdee"] == 2759
    
    # Verify Lose Weight Goal (-500) -> 2259
    assert data["daily_calories"] == 2259
