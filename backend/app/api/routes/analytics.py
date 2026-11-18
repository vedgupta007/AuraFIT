from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user

router = APIRouter()

@router.get("/personal-records", response_model=Dict[str, Any])
async def get_personal_records(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    user_id = str(current_user["_id"])
    workouts = await db.workouts.find({"user_id": user_id}).to_list(length=None)
    
    records = {}
    for w in workouts:
        for ex in w.get("exercises", []):
            name = ex.get("exercise_name")
            weight = ex.get("weight_kg", 0)
            reps = ex.get("reps", 0)
            
            if not name or weight is None:
                continue
                
            if name not in records:
                records[name] = {"max_weight": weight, "max_reps": reps, "date": w.get("started_at")}
            else:
                if weight > records[name]["max_weight"]:
                    records[name] = {"max_weight": weight, "max_reps": reps, "date": w.get("started_at")}
                elif weight == records[name]["max_weight"] and reps > records[name]["max_reps"]:
                    records[name] = {"max_weight": weight, "max_reps": reps, "date": w.get("started_at")}
                    
    return {"records": records}

@router.get("/weekly-summary", response_model=Dict[str, Any])
async def get_weekly_summary(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    user_id = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    
    # Workouts
    workouts = await db.workouts.find({
        "user_id": user_id, 
        "started_at": {"$gte": seven_days_ago}
    }).to_list(length=None)
    
    # Nutrition
    meals = await db.meals.find({
        "user_id": user_id, 
        "consumed_at": {"$gte": seven_days_ago}
    }).to_list(length=None)
    
    total_cals = sum(m.get("calories", 0) for m in meals)
    total_protein = sum(m.get("protein_grams", 0) for m in meals)
    
    return {
        "workouts_completed": len(workouts),
        "avg_daily_calories": total_cals // 7,
        "avg_daily_protein": round(total_protein / 7, 1),
        "total_meals_logged": len(meals)
    }