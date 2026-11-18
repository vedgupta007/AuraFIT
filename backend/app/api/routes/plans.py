from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.core.config import settings
from app.models.domain import (
    MealPlanUpdate, MealPlanResponse,
    WorkoutPlanUpdate, WorkoutPlanResponse,
    FitnessPlanStrategyUpdate, FitnessPlanStrategyResponse
)
from pydantic import BaseModel
from bson import ObjectId
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)
router = APIRouter()

def handle_ai_error(e: Exception, context_msg: str):
    error_str = str(e)
    logger.error(f"{context_msg}: {error_str}")
    if "404" in error_str or "NOT_FOUND" in error_str:
        raise HTTPException(status_code=404, detail="The configured AI model is currently unavailable.")
    elif "429" in error_str or "quota" in error_str.lower():
        raise HTTPException(status_code=429, detail="The AI Coach is receiving too many requests or has exceeded its quota. Please wait.")
    elif "400" in error_str or "API_KEY_INVALID" in error_str:
        raise HTTPException(status_code=500, detail="AI generation failed due to a provider configuration issue.")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate at this time. Please try again.")

# -------------------------------------
# FITNESS STRATEGY PLAN
# -------------------------------------

@router.get("/strategy", response_model=FitnessPlanStrategyResponse)
async def get_fitness_strategy(current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    plan = await db.fitness_plans.find_one(
        {"user_id": str(current_user["_id"]), "status": {"$in": ["generated", "accepted"]}},
        sort=[("created_at", -1)]
    )
    if not plan:
        raise HTTPException(status_code=404, detail="No active fitness plan found")
    plan["id"] = str(plan["_id"])
    return plan

@router.post("/strategy/generate", response_model=FitnessPlanStrategyResponse)
async def generate_fitness_strategy(current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required to generate plan")
        
    missing_fields = []
    for field in ['goal', 'training_experience', 'preferred_workout_frequency', 'dietary_preference']:
        if not profile.get(field):
            missing_fields.append(field.replace('_', ' ').title())
            
    if missing_fields:
        raise HTTPException(status_code=422, detail=f"Please update your profile. Missing: {', '.join(missing_fields)}")
    
    prompt = f"""
    You are an expert fitness AI. Generate a personalized fitness strategy for this user:
    Goal: {profile.get('goal')}
    Experience: {profile.get('training_experience')}
    Frequency: {profile.get('preferred_workout_frequency')}x per week
    Diet: {profile.get('dietary_preference')}
    
    Return JSON ONLY with this exact format:
    {{
        "strategy_text": "Detailed 2-paragraph overall strategy...",
        "nutrition_protocol": "Specific nutrition guidance based on their diet and goal...",
        "training_protocol": "Specific workout guidance based on their experience and frequency..."
    }}
    """
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text)
    except Exception as e:
        handle_ai_error(e, "Strategy Gen")
        
    plan_dict = {
        "user_id": str(current_user["_id"]),
        "strategy_text": data.get("strategy_text", "Generated Strategy"),
        "nutrition_protocol": data.get("nutrition_protocol", "Generated Nutrition Protocol"),
        "training_protocol": data.get("training_protocol", "Generated Training Protocol"),
        "status": "generated",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.fitness_plans.insert_one(plan_dict)
    plan_dict["id"] = str(result.inserted_id)
    return plan_dict

@router.patch("/strategy/{plan_id}", response_model=FitnessPlanStrategyResponse)
async def update_fitness_strategy(plan_id: str, update: FitnessPlanStrategyUpdate, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.fitness_plans.find_one_and_update(
        {"_id": ObjectId(plan_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")
    result["id"] = str(result["_id"])
    return result

# -------------------------------------
# WORKOUT PLANS
# -------------------------------------

@router.get("/workouts", response_model=List[WorkoutPlanResponse])
async def get_workout_plans(start_date: str = None, end_date: str = None, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    query = {"user_id": str(current_user["_id"])}
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    
    plans = []
    async for p in db.workout_plans.find(query).sort("date", 1):
        p["id"] = str(p["_id"])
        plans.append(p)
    return plans

@router.get("/workouts/today", response_model=WorkoutPlanResponse)
async def get_today_workout_plan(current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    today = datetime.utcnow().date().isoformat()
    plan = await db.workout_plans.find_one({"user_id": str(current_user["_id"]), "date": today, "status": {"$in": ["generated", "accepted"]}})
    if not plan:
        raise HTTPException(status_code=404, detail="No workout scheduled for today")
    plan["id"] = str(plan["_id"])
    return plan

@router.post("/workouts/generate", response_model=WorkoutPlanResponse)
async def generate_workout_plan(target_date: str, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required to generate workout plan")
        
    missing_fields = []
    for field in ['goal', 'training_experience']:
        if not profile.get(field):
            missing_fields.append(field.title())
            
    if missing_fields:
        raise HTTPException(status_code=422, detail=f"Please update your profile. Missing: {', '.join(missing_fields)}")
    
    prompt = f"""
    Generate a workout plan for someone with goal: {profile.get('goal')}.
    Experience level: {profile.get('training_experience')}.
    Ensure the workout is realistic and clearly structured.
    
    Return ONLY raw JSON in this exact format:
    {{
        "workout_title": "Full Body Strength",
        "focus": "Hypertrophy and functional movement",
        "estimated_duration_minutes": 45,
        "exercises": [
            {{
                "exercise_name": "Barbell Squat", 
                "sets": 3, 
                "reps": 10, 
                "weight_kg": 0, 
                "duration": 0, 
                "rest": 60, 
                "completed": false,
                "guidance": {{
                    "starting_position": "Stand with feet shoulder-width apart...",
                    "execution": "Lower your hips...",
                    "breathing": "Inhale down, exhale up",
                    "common_mistakes": "Knees caving in, rounding back",
                    "safety": "Stop if you feel sharp pain in knees or lower back"
                }}
            }}
        ]
    }}
    """
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        res = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(res.text)
    except Exception as e:
        handle_ai_error(e, "Workout Gen")
        
    plan = {
        "user_id": str(current_user["_id"]),
        "date": target_date,
        "workout_title": data.get("workout_title", "Daily Workout"),
        "focus": data.get("focus", "General"),
        "exercises": data.get("exercises", []),
        "estimated_duration_minutes": data.get("estimated_duration_minutes", 45),
        "status": "generated",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.workout_plans.insert_one(plan)
    plan["id"] = str(result.inserted_id)
    return plan

@router.patch("/workouts/{plan_id}", response_model=WorkoutPlanResponse)
async def update_workout_plan(plan_id: str, update: WorkoutPlanUpdate, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.workout_plans.find_one_and_update(
        {"_id": ObjectId(plan_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")
    result["id"] = str(result["_id"])
    return result

@router.post("/workouts/{plan_id}/complete")
async def complete_workout_plan(plan_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    plan = await db.workout_plans.find_one({"_id": ObjectId(plan_id), "user_id": str(current_user["_id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    await db.workout_plans.update_one({"_id": ObjectId(plan_id)}, {"$set": {"status": "completed", "updated_at": datetime.utcnow()}})
    
    workout_log = {
        "user_id": str(current_user["_id"]),
        "title": plan["workout_title"],
        "started_at": datetime.utcnow(),
        "ended_at": datetime.utcnow(),
        "notes": f"Completed from plan: {plan['focus']}",
        "exercises": [
            {
                "exercise_name": ex["exercise_name"],
                "sets": ex.get("sets", 0),
                "reps": ex.get("reps", 0),
                "weight_kg": ex.get("weight_kg", 0),
                "duration_minutes": ex.get("duration", 0),
                "notes": ""
            } for ex in plan.get("exercises", [])
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.workouts.insert_one(workout_log)
    return {"status": "success", "message": "Workout completed and saved to log"}

# -------------------------------------
# MEAL PLANS
# -------------------------------------

@router.get("/meals", response_model=List[MealPlanResponse])
async def get_meal_plans(start_date: str = None, end_date: str = None, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    query = {"user_id": str(current_user["_id"])}
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    
    plans = []
    async for p in db.meal_plans.find(query).sort("date", 1):
        p["id"] = str(p["_id"])
        plans.append(p)
    return plans

@router.post("/meals/generate", response_model=MealPlanResponse)
async def generate_meal_plan(target_date: str, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required to generate meal plan")
        
    missing_fields = []
    for field in ['dietary_preference']:
        if not profile.get(field):
            missing_fields.append(field.replace('_', ' ').title())
            
    if missing_fields:
        raise HTTPException(status_code=422, detail=f"Please update your profile. Missing: {', '.join(missing_fields)}")
        
    allergies = profile.get("allergies", [])
    disliked = profile.get("disliked_foods", [])
    
        # Calculate Targets
    weight = profile.get("weight_kg", 70)
    height = profile.get("height_cm", 170)
    age = profile.get("age", 30)
    sex = profile.get("sex", "M")
    
    if sex == "M":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
    tdee = bmr * 1.55 # Assume moderate for baseline if missing logic
    goal = profile.get("goal", "maintain_weight")
    
    daily_calories = tdee
    if goal == "lose_weight": daily_calories = tdee - 500
    elif goal == "gain_muscle": daily_calories = tdee + 500
    if daily_calories < 1200: daily_calories = 1200
    
    daily_calories = int(round(daily_calories))
    daily_protein = round((daily_calories * 0.30) / 4)
    daily_fat = round((daily_calories * 0.25) / 9)
    daily_carbs = round((daily_calories * 0.45) / 4)
    daily_fiber = 30 # Generic fiber target
    
    prompt = f"""
    Generate a full daily meal plan tailored EXACTLY to these macros:
    - Calories: ~{daily_calories} kcal
    - Protein: ~{daily_protein}g
    - Carbs: ~{daily_carbs}g
    - Fats: ~{daily_fat}g
    - Fiber: ~{daily_fiber}g
    
    Dietary preference: {profile.get('dietary_preference')}.
    Allergies: {', '.join(allergies) if allergies else 'None'}.
    Disliked Foods: {', '.join(disliked) if disliked else 'None'}.
    
    NOTE: Ensure the generated meals sum up to closely match the requested target macros. Provide approximate estimates.
    
    Return ONLY raw JSON in this exact format:
    {{
        "total_calories": {daily_calories},
        "total_protein": {daily_protein},
        "total_carbs": {daily_carbs},
        "total_fats": {daily_fat},
        "total_fiber": {daily_fiber},
        "meals": [
            {{
                "meal_type": "breakfast", 
                "meal_name": "Oatmeal with Protein Powder", 
                "calories": 400, 
                "protein": 30, 
                "carbs": 50, 
                "fats": 10,
                "fiber": 5,
                "ingredients": ["1/2 cup oats", "1 scoop protein", "1 cup almond milk"],
                "status": "generated"
            }}
        ]
    }}
    Ensure meal types are strictly 'breakfast', 'lunch', 'dinner', or 'snack'.
    """
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        res = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(res.text)
    except Exception as e:
        handle_ai_error(e, "Meal Gen")
        
    # Recalculate totals directly from generated meals to ensure honesty
    generated_meals = data.get("meals", [])
    gen_cals = sum([m.get("calories", 0) for m in generated_meals])
    gen_prot = sum([m.get("protein", 0) for m in generated_meals])
    gen_carbs = sum([m.get("carbs", 0) for m in generated_meals])
    gen_fats = sum([m.get("fats", 0) for m in generated_meals])
    gen_fiber = sum([m.get("fiber", 0) for m in generated_meals])
        
    plan = {
        "user_id": str(current_user["_id"]),
        "date": target_date,
        "meals": generated_meals,
        "total_calories": gen_cals,
        "total_protein": gen_prot,
        "total_carbs": gen_carbs,
        "total_fats": gen_fats,
        "total_fiber": gen_fiber,
        "target_calories": daily_calories,
        "target_protein": daily_protein,
        "target_carbs": daily_carbs,
        "target_fats": daily_fat,
        "target_fiber": daily_fiber,
        "status": "generated",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.meal_plans.insert_one(plan)
    plan["id"] = str(result.inserted_id)
    return plan

@router.patch("/meals/{plan_id}", response_model=MealPlanResponse)
async def update_meal_plan(plan_id: str, update: MealPlanUpdate, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.meal_plans.find_one_and_update(
        {"_id": ObjectId(plan_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")
    result["id"] = str(result["_id"])
    return result

@router.post("/meals/{plan_id}/log")
async def log_meal_plan_to_diary(plan_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    plan = await db.meal_plans.find_one({"_id": ObjectId(plan_id), "user_id": str(current_user["_id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    await db.meal_plans.update_one({"_id": ObjectId(plan_id)}, {"$set": {"status": "completed", "updated_at": datetime.utcnow()}})
    
    dt = datetime.fromisoformat(plan["date"]) if "T" not in plan["date"] else datetime.fromisoformat(plan["date"].split("T")[0])
    
    docs = []
    for m in plan.get("meals", []):
        if m.get("status") != "rejected":
            docs.append({
                "user_id": str(current_user["_id"]),
                "meal_type": m.get("meal_type", "snack").lower(),
                "meal_name": m.get("meal_name", "Planned Meal"),
                "consumed_at": dt,
                "serving_size": "1 serving",
                "calories": m.get("calories", 0),
                "protein_grams": m.get("protein", 0),
                "carbohydrates_grams": m.get("carbs", 0),
                "fat_grams": m.get("fats", 0),
                "fiber_grams": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
    
    if docs:
        await db.meals.insert_many(docs)
        
    return {"status": "success", "message": f"{len(docs)} meals logged to your diary"}


class AlternativeRequest(BaseModel):
    food_name: str
    target_calories: Optional[int] = None

class AlternativeOption(BaseModel):
    meal_name: str
    calories: int
    protein: float
    carbs: float
    fats: float
    ingredients: List[str]
    reason: str

@router.post("/meals/alternatives", response_model=List[AlternativeOption])
async def get_food_alternatives(request: AlternativeRequest, current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    
    prompt = f"""
    Suggest 3 healthy food/meal alternatives for: "{request.food_name}".
    Target Calories around: {request.target_calories if request.target_calories else 'similar to original'}.
    Dietary Preference: {profile.get('dietary_preference') if profile else 'none'}.
    Allergies: {', '.join(profile.get('allergies', [])) if profile else 'none'}.
    
    Return ONLY raw JSON in this exact format (an array of objects):
    [
        {{
            "meal_name": "...",
            "calories": 300,
            "protein": 20,
            "carbs": 30,
            "fats": 10,
            "ingredients": ["..."],
            "reason": "Why this is a good swap"
        }}
    ]
    """
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        res = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(res.text)
        return data
    except Exception as e:
        handle_ai_error(e, "Alternatives Gen")



@router.post("/workouts/guidance")
async def get_workout_guidance(
    payload: dict,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    exercise_name = payload.get("exercise_name")
    workout_focus = payload.get("workout_focus", "General fitness")
    if not exercise_name:
        raise HTTPException(status_code=400, detail="Exercise name is required")
        
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    experience = profile.get("training_experience", "intermediate") if profile else "intermediate"
    goal = profile.get("goal", "improve fitness") if profile else "improve fitness"
    
    prompt = f"""
    Provide workout guidance for the exercise '{exercise_name}'.
    The user's goal is: {goal}.
    The user's experience level is: {experience}.
    The workout focus is: {workout_focus}.
    
    Provide safe, accurate, and helpful step-by-step guidance.
    
    Return ONLY raw JSON in this exact format:
    {{
        "starting_position": "Detailed description...",
        "execution": "Detailed description...",
        "breathing": "How to breathe...",
        "common_mistakes": "What to avoid...",
        "safety": "Safety tips..."
    }}
    """
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        res = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(res.text)
        return data
    except Exception as e:
        # Fallback if AI fails
        return {
            "starting_position": f"Prepare for {exercise_name} with proper posture.",
            "execution": f"Perform {exercise_name} with controlled movement, focusing on the target muscles.",
            "breathing": "Inhale during the eccentric phase, exhale during the concentric phase.",
            "common_mistakes": "Rushing the movement, using momentum, or breaking form.",
            "safety": "Stop immediately if you feel sharp joint pain. Use an appropriate weight."
        }


