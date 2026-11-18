from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import AchievementResponse

router = APIRouter()

ACHIEVEMENTS_DEF = [
    {"key": "first_workout", "title": "First Step", "description": "Log your first workout."},
    {"key": "first_meal", "title": "Nutrition Focus", "description": "Log your first meal."},
    {"key": "ten_workouts", "title": "Consistency Is Key", "description": "Log 10 workouts."},
]

@router.get("/", response_model=List[AchievementResponse])
async def get_achievements(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    user_id = str(current_user["_id"])
    achievements = await db.achievements.find({"user_id": user_id}).to_list(length=None)
    
    result = []
    for a in achievements:
        result.append({
            "id": str(a["_id"]),
            "user_id": a["user_id"],
            "title": a["title"],
            "description": a["description"],
            "key": a["key"],
            "earned_at": a["earned_at"]
        })
    return result

@router.post("/evaluate")
async def evaluate_achievements(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    user_id = str(current_user["_id"])
    newly_earned = []
    now = datetime.now(timezone.utc)
    
    # Existing
    existing_cursor = await db.achievements.find({"user_id": user_id}).to_list(length=None)
    existing_keys = {a["key"] for a in existing_cursor}
    
    # Checks
    if "first_workout" not in existing_keys:
        workout_count = await db.workouts.count_documents({"user_id": user_id})
        if workout_count >= 1:
            newly_earned.append(ACHIEVEMENTS_DEF[0])
            
    if "first_meal" not in existing_keys:
        meal_count = await db.meals.count_documents({"user_id": user_id})
        if meal_count >= 1:
            newly_earned.append(ACHIEVEMENTS_DEF[1])
            
    if "ten_workouts" not in existing_keys:
        workout_count = await db.workouts.count_documents({"user_id": user_id})
        if workout_count >= 10:
            newly_earned.append(ACHIEVEMENTS_DEF[2])
            
    for ach in newly_earned:
        await db.achievements.insert_one({
            "user_id": user_id,
            "key": ach["key"],
            "title": ach["title"],
            "description": ach["description"],
            "earned_at": now
        })
        
    return {"new_achievements": newly_earned}