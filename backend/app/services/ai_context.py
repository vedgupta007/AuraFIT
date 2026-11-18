from typing import Dict, Any
from app.db.mongodb import get_database
from bson import ObjectId
from app.api.routes.nutrition import get_nutrition_goals

async def build_user_context(user_id: str, db) -> Dict[str, Any]:
    # Fetch profile
    profile = await db.profiles.find_one({"user_id": ObjectId(user_id)})
    if not profile:
        return {"error": "Profile not configured"}
        
    # Get calculated goals
    # We can invoke the logic directly. get_nutrition_goals logic is in nutrition route or we can just use the profile fields directly 
    # to calculate. To avoid duplicate code, let's implement the core BMR formula here or extract it if it's not isolated.
    # Let's just extract the BMR/TDEE math here based on the profile since we just need the numbers.
    weight = profile.get("weight_kg", 0)
    height = profile.get("height_cm", 0)
    age = profile.get("age", 0)
    sex = profile.get("sex", "M")
    
    if weight and height and age:
        # Mifflin-St Jeor
        bmr = (10 * weight) + (6.25 * height) - (5 * age)
        bmr += 5 if sex == "M" else -161
        
        multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        activity = profile.get("activity_level", "moderate")
        tdee = int(bmr * multipliers.get(activity, 1.2))
        
        goal = profile.get("goal", "maintain_weight")
        if goal == "lose_weight":
            daily_calories = tdee - 500
        elif goal == "gain_muscle":
            daily_calories = tdee + 300
        else:
            daily_calories = tdee
            
        protein = weight * 2.0
    else:
        bmr, tdee, daily_calories, protein = None, None, None, None

    context = {
        "profile": {
            "age": age,
            "sex": sex,
            "weight_kg": weight,
            "height_cm": height,
            "goal": profile.get("goal"),
            "activity_level": profile.get("activity_level"),
            "dietary_preference": profile.get("dietary_preference"),
            "allergies": profile.get("allergies", []),
            "disliked_foods": profile.get("disliked_foods", []),
            "training_experience": profile.get("training_experience")
        },
        "targets": {
            "bmr": int(bmr) if bmr else None,
            "tdee": tdee,
            "daily_calories": daily_calories,
            "daily_protein": protein
        }
    }
    
    # Fetch recent meals (e.g. from today)
    # This requires timezone logic, but for AI context just the last 10 meals is helpful enough
    recent_meals = await db.meals.find({"user_id": ObjectId(user_id)}).sort("consumed_at", -1).limit(5).to_list(length=5)
    
    context["recent_meals"] = [
        {
            "id": str(m["_id"]),
            "name": m.get("meal_name"),
            "calories": m.get("calories"),
            "protein": m.get("protein_grams"),
            "consumed_at": m.get("consumed_at")
        } for m in recent_meals
    ]
    
    # Phase 6 Core additions
    recent_workouts = await db.workouts.find({"user_id": str(user_id)}).sort("started_at", -1).limit(5).to_list(length=5)
    context["recent_workouts"] = [
        {
            "id": str(w["_id"]),
            "title": w.get("title"),
            "started_at": w.get("started_at"),
            "notes": w.get("notes")
        } for w in recent_workouts
    ]

    active_goals = await db.goals.find({"user_id": str(user_id), "status": "active"}).to_list(length=5)
    context["active_goals"] = [
        {
            "id": str(g["_id"]),
            "title": g.get("title"),
            "goal_type": g.get("goal_type")
        } for g in active_goals
    ]
    
    recent_measurements = await db.measurements.find({"user_id": str(user_id)}).sort("date", -1).limit(3).to_list(length=3)
    context["recent_measurements"] = [
        {
            "id": str(m["_id"]),
            "date": m.get("date"),
            "weight_kg": m.get("weight_kg"),
            "body_fat_percent": m.get("body_fat_percent")
        } for m in recent_measurements
    ]

    # PRs
    # Very heavy aggregate query, simple approximate here
    # A single heavy PR summary could be passed
    context["has_achievements"] = bool(await db.achievements.count_documents({"user_id": str(user_id)}))

    return context
