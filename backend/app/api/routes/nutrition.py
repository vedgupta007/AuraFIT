from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import MealCreate, MealUpdate, MealResponse, DailySummaryResponse, NutritionGoalsResponse

router = APIRouter()
from app.models.domain import SavedMealCreate, SavedMealResponse

def serialize_saved_meal(meal: dict) -> dict:
    return {
        "id": str(meal["_id"]),
        "user_id": str(meal["user_id"]),
        "meal_name": meal["meal_name"],
        "meal_type": meal["meal_type"],
        "serving_size": meal["serving_size"],
        "calories": meal["calories"],
        "protein_grams": meal["protein_grams"],
        "carbohydrates_grams": meal["carbohydrates_grams"],
        "fat_grams": meal["fat_grams"],
        "fiber_grams": meal["fiber_grams"],
        "ingredients": meal.get("ingredients", []),
        "notes": meal.get("notes"),
        "created_at": meal["created_at"],
        "updated_at": meal["updated_at"]
    }

@router.post("/saved-meals", response_model=SavedMealResponse, status_code=status.HTTP_201_CREATED)
async def create_saved_meal(meal: SavedMealCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    meal_dict = meal.model_dump()
    meal_dict["user_id"] = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    meal_dict["created_at"] = now
    meal_dict["updated_at"] = now
    result = await db.saved_meals.insert_one(meal_dict)
    meal_dict["_id"] = result.inserted_id
    return serialize_saved_meal(meal_dict)

@router.get("/saved-meals", response_model=List[SavedMealResponse])
async def get_saved_meals(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    cursor = db.saved_meals.find({"user_id": str(current_user["_id"])}).sort("created_at", -1)
    meals = await cursor.to_list(length=100)
    return [serialize_saved_meal(m) for m in meals]

@router.delete("/saved-meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_meal(meal_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    from bson import ObjectId
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=400, detail="Invalid meal ID format")
    result = await db.saved_meals.delete_one({"_id": ObjectId(meal_id), "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Saved meal not found")
    return None

def serialize_meal(meal: dict) -> dict:
    return {
        "id": str(meal["_id"]),
        "user_id": str(meal["user_id"]),
        "meal_type": meal["meal_type"],
        "meal_name": meal["meal_name"],
        "consumed_at": meal["consumed_at"],
        "serving_size": meal["serving_size"],
        "calories": meal["calories"],
        "protein_grams": meal["protein_grams"],
        "carbohydrates_grams": meal["carbohydrates_grams"],
        "fat_grams": meal["fat_grams"],
        "fiber_grams": meal["fiber_grams"],
        "notes": meal.get("notes"),
        "created_at": meal["created_at"],
        "updated_at": meal["updated_at"]
    }

@router.post("/meals", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal: MealCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    now = datetime.now(timezone.utc)
    meal_dict = meal.model_dump()
    
    # Force associate with authenticated user
    meal_dict["user_id"] = current_user["_id"]
    meal_dict["created_at"] = now
    meal_dict["updated_at"] = now
    
    result = await db.meals.insert_one(meal_dict)
    
    created_meal = await db.meals.find_one({"_id": result.inserted_id})
    return serialize_meal(created_meal)

@router.get("/meals", response_model=List[MealResponse])
async def get_meals(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    meal_type: Optional[str] = Query(None, pattern="^(breakfast|lunch|dinner|snack)$"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    query = {"user_id": current_user["_id"]}
    
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = start_date
        if end_date:
            date_query["$lte"] = end_date
        query["consumed_at"] = date_query
        
    if meal_type:
        query["meal_type"] = meal_type
        
    cursor = db.meals.find(query).sort("consumed_at", -1).skip(skip).limit(limit)
    meals = await cursor.to_list(length=limit)
    
    return [serialize_meal(meal) for meal in meals]

@router.get("/meals/{meal_id}", response_model=MealResponse)
async def get_meal(
    meal_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=404, detail="Meal not found")
        
    meal = await db.meals.find_one({"_id": ObjectId(meal_id), "user_id": current_user["_id"]})
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    return serialize_meal(meal)

@router.patch("/meals/{meal_id}", response_model=MealResponse)
async def update_meal(
    meal_id: str,
    meal_update: MealUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=404, detail="Meal not found")
        
    # Check ownership
    existing_meal = await db.meals.find_one({"_id": ObjectId(meal_id), "user_id": current_user["_id"]})
    if not existing_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    update_data = {k: v for k, v in meal_update.model_dump().items() if v is not None}
    
    if not update_data:
        return serialize_meal(existing_meal)
        
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    await db.meals.update_one(
        {"_id": ObjectId(meal_id)},
        {"$set": update_data}
    )
    
    updated_meal = await db.meals.find_one({"_id": ObjectId(meal_id)})
    return serialize_meal(updated_meal)

@router.delete("/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
    meal_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=404, detail="Meal not found")
        
    result = await db.meals.delete_one({"_id": ObjectId(meal_id), "user_id": current_user["_id"]})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    return None

@router.get("/daily-summary", response_model=DailySummaryResponse)
async def get_daily_summary(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    tz_offset_minutes: int = Query(0, description="Timezone offset from UTC in minutes (e.g. -300 for EST)"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    try:
        from datetime import timedelta
        local_start = datetime.strptime(date, "%Y-%m-%d")
        start_of_day = (local_start - timedelta(minutes=tz_offset_minutes)).replace(tzinfo=timezone.utc)
        
        local_end = datetime.strptime(f"{date} 23:59:59", "%Y-%m-%d %H:%M:%S")
        end_of_day = (local_end - timedelta(minutes=tz_offset_minutes)).replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
    # Query meals for this user within this day
    cursor = db.meals.find({
        "user_id": current_user["_id"],
        "consumed_at": {"$gte": start_of_day, "$lte": end_of_day}
    })
    
    meals = await cursor.to_list(length=100) # Unlikely to have more than 100 meals in a single day
    
    summary = {
        "date": date,
        "total_calories": 0,
        "total_protein": 0.0,
        "total_carbohydrates": 0.0,
        "total_fat": 0.0,
        "total_fiber": 0.0,
        "meal_count": len(meals)
    }
    
    for meal in meals:
        summary["total_calories"] += meal.get("calories", 0)
        summary["total_protein"] += meal.get("protein_grams", 0.0)
        summary["total_carbohydrates"] += meal.get("carbohydrates_grams", 0.0)
        summary["total_fat"] += meal.get("fat_grams", 0.0)
        summary["total_fiber"] += meal.get("fiber_grams", 0.0)
        
    # Round floats to 1 decimal place to prevent floating point artifacts
    summary["total_protein"] = round(summary["total_protein"], 1)
    summary["total_carbohydrates"] = round(summary["total_carbohydrates"], 1)
    summary["total_fat"] = round(summary["total_fat"], 1)
    summary["total_fiber"] = round(summary["total_fiber"], 1)
        
    return summary

@router.get("/goals", response_model=NutritionGoalsResponse)
async def get_nutrition_goals(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found, please complete onboarding.")

    # Calculate BMR
    # Mifflin-St Jeor Equation
    # Men: 10 * weight (kg) + 6.25 * height (cm) - 5 * age + 5
    # Women: 10 * weight (kg) + 6.25 * height (cm) - 5 * age - 161
    weight = profile.get("weight_kg", 0)
    height = profile.get("height_cm", 0)
    age = profile.get("age", 0)
    sex = profile.get("sex", "M")

    if sex == "M":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif sex == "F":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        # Average for 'Other'
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 78

    # Calculate TDEE
    activity_level = profile.get("activity_level", "sedentary")
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    tdee = bmr * multipliers.get(activity_level, 1.2)

    # Goals calculation
    goal = profile.get("goal", "maintain_weight")
    daily_calories = tdee
    if goal == "lose_weight":
        daily_calories = tdee - 500
    elif goal == "gain_muscle":
        daily_calories = tdee + 500
        
    # Prevent extreme low calories
    if daily_calories < 1200:
        daily_calories = 1200
        
    daily_calories = int(round(daily_calories))
    
    # Macros
    # Protein: 30%
    # Fat: 25%
    # Carbs: 45%
    daily_protein = (daily_calories * 0.30) / 4
    daily_fat = (daily_calories * 0.25) / 9
    daily_carbohydrates = (daily_calories * 0.45) / 4
    daily_fiber = 30.0

    return {
        "bmr": int(round(bmr)),
        "tdee": int(round(tdee)),
        "daily_calories": daily_calories,
        "daily_protein": round(daily_protein, 1),
        "daily_carbohydrates": round(daily_carbohydrates, 1),
        "daily_fat": round(daily_fat, 1),
        "daily_fiber": round(daily_fiber, 1)
    }

