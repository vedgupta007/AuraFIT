from typing import Dict, Any, List
from bson import ObjectId

async def search_foods_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    search = args.get("search")
    category = args.get("category")
    
    query = {"is_active": True}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = category
        
    profile = user_context.get("profile", {})
    diet = profile.get("dietary_preference", "")
    allergies = [a.lower() for a in profile.get("allergies", [])]
    
    if diet == "vegetarian":
        query["is_vegetarian"] = True
    elif diet == "vegan":
        query["is_vegan"] = True
    elif diet == "eggetarian":
        query["is_eggetarian"] = True
        
    foods = await db.foods.find(query).limit(5).to_list(length=5)
    
    safe_foods = []
    for f in foods:
        f_allergens = [a.lower() for a in f.get("allergens", [])]
        if any(user_allergy in f_allergens for user_allergy in allergies):
            continue
        safe_foods.append({
            "id": str(f["_id"]),
            "name": f["name"],
            "category": f["category"],
            "calories": f["calories"],
            "protein": f["protein"],
            "serving": f"{f['serving_size']} {f['serving_unit']}"
        })
        
    if not safe_foods:
        return {"results": [], "message": "No foods found matching criteria and safety constraints."}
    return {"results": safe_foods}

async def get_food_details_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    food_id = args.get("food_id")
    if not ObjectId.is_valid(food_id):
        return {"error": "Invalid food_id format"}
    
    food = await db.foods.find_one({"_id": ObjectId(food_id), "is_active": True})
    if not food:
        return {"error": "Food not found in database"}
        
    return {
        "id": str(food["_id"]),
        "name": food["name"],
        "category": food["category"],
        "calories": food["calories"],
        "protein": food["protein"],
        "carbohydrates": food.get("carbohydrates", 0),
        "fat": food.get("fat", 0),
        "fiber": food.get("fiber", 0),
        "serving": f"{food['serving_size']} {food['serving_unit']}",
        "allergens": food.get("allergens", []),
        "is_vegan": food.get("is_vegan", False),
        "is_vegetarian": food.get("is_vegetarian", False)
    }

async def find_alternative_food_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    food_id = args.get("food_id")
    if not ObjectId.is_valid(food_id):
        return {"error": "Invalid food_id format"}
        
    food = await db.foods.find_one({"_id": ObjectId(food_id), "is_active": True})
    if not food:
        return {"error": "Original food not found"}
        
    # Same category, similar protein, exclude self
    query = {
        "is_active": True, 
        "_id": {"$ne": ObjectId(food_id)},
        "category": food["category"]
    }
    
    profile = user_context.get("profile", {})
    diet = profile.get("dietary_preference", "")
    allergies = [a.lower() for a in profile.get("allergies", [])]
    
    if diet == "vegetarian":
        query["is_vegetarian"] = True
    elif diet == "vegan":
        query["is_vegan"] = True
    elif diet == "eggetarian":
        query["is_eggetarian"] = True
        
    candidates = await db.foods.find(query).limit(10).to_list(length=10)
    
    safe_foods = []
    for f in candidates:
        f_allergens = [a.lower() for a in f.get("allergens", [])]
        if any(user_allergy in f_allergens for user_allergy in allergies):
            continue
        safe_foods.append({
            "id": str(f["_id"]),
            "name": f["name"],
            "calories": f["calories"],
            "protein": f["protein"]
        })
        
    if not safe_foods:
        return {"results": [], "message": "No safe alternatives found in this category."}
    return {"results": safe_foods[:3]}

async def search_exercises_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    search = args.get("search")
    muscle = args.get("muscle")
    equipment = args.get("equipment")
    
    query = {"is_active": True}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if muscle:
        query["primary_muscle"] = {"$regex": muscle, "$options": "i"}
    if equipment:
        query["equipment"] = {"$regex": equipment, "$options": "i"}
        
    exercises = await db.exercises.find(query).limit(5).to_list(length=5)
    
    results = []
    for ex in exercises:
        results.append({
            "id": str(ex["_id"]),
            "name": ex["name"],
            "muscle": ex["primary_muscle"],
            "equipment": ex["equipment"],
            "difficulty": ex["difficulty"]
        })
        
    if not results:
        return {"results": [], "message": "No exercises found."}
    return {"results": results}

async def get_exercise_details_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    exercise_id = args.get("exercise_id")
    if not ObjectId.is_valid(exercise_id):
        return {"error": "Invalid exercise_id format"}
    
    ex = await db.exercises.find_one({"_id": ObjectId(exercise_id), "is_active": True})
    if not ex:
        return {"error": "Exercise not found"}
        
    return {
        "id": str(ex["_id"]),
        "name": ex["name"],
        "primary_muscle": ex["primary_muscle"],
        "secondary_muscles": ex.get("secondary_muscles", []),
        "equipment": ex["equipment"],
        "difficulty": ex["difficulty"],
        "instructions": ex.get("instructions", []),
        "tips": ex.get("tips", [])
    }

async def find_alternative_exercise_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    exercise_id = args.get("exercise_id")
    if not ObjectId.is_valid(exercise_id):
        return {"error": "Invalid exercise_id format"}
        
    ex = await db.exercises.find_one({"_id": ObjectId(exercise_id), "is_active": True})
    if not ex:
        return {"error": "Original exercise not found"}
        
    query = {
        "is_active": True, 
        "_id": {"$ne": ObjectId(exercise_id)},
        "primary_muscle": ex["primary_muscle"]
    }
    
    # Try to find something with different equipment (e.g. Bodyweight instead of Machine)
    candidates = await db.exercises.find(query).limit(5).to_list(length=5)
    results = []
    for c in candidates:
        results.append({
            "id": str(c["_id"]),
            "name": c["name"],
            "equipment": c["equipment"],
            "difficulty": c["difficulty"]
        })
        
    return {"results": results[:3]}

async def get_current_plan_tool(db, args: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for a real plan tool. For now, fetch recent meals to represent current plan.
    user_id = user_context.get("user_id")
    if not user_id:
        return {"error": "User ID not found in context"}
        
    recent_meals = await db.meals.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(10).to_list(length=10)
    
    results = []
    for m in recent_meals:
        results.append({
            "meal_id": str(m["_id"]),
            "meal_name": m.get("meal_name", ""),
            "calories": m.get("calories", 0)
        })
        
    return {"current_tracked_meals": results}

async def replace_food_in_plan_tool(db, args: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    meal_id = args.get("meal_id")
    new_food_id = args.get("new_food_id")
    
    if not ObjectId.is_valid(meal_id) or not ObjectId.is_valid(new_food_id):
        return {"error": "Invalid IDs"}
        
    meal = await db.meals.find_one({"_id": ObjectId(meal_id), "user_id": ObjectId(user_id)})
    if not meal:
        return {"error": "Meal not found or not owned by user"}
        
    food = await db.foods.find_one({"_id": ObjectId(new_food_id), "is_active": True})
    if not food:
        return {"error": "Food not found in database"}
        
    await db.meals.update_one(
        {"_id": ObjectId(meal_id)},
        {"$set": {
            "meal_name": food["name"],
            "calories": food["calories"],
            "protein_grams": food["protein"],
            "carbohydrates_grams": food["carbohydrates"],
            "fat_grams": food["fat"],
            "fiber_grams": food["fiber"]
        }}
    )
    
    return {"success": True, "message": f"Successfully updated meal to {food['name']}"}

async def replace_exercise_in_plan_tool(db, args: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    return {"error": "Exercise plan modification is not yet implemented (Phase 6)."}

TOOLS_REGISTRY = {
    "search_foods": search_foods_tool,
    "get_food_details": get_food_details_tool,
    "find_alternative_food": find_alternative_food_tool,
    "search_exercises": search_exercises_tool,
    "get_exercise_details": get_exercise_details_tool,
    "find_alternative_exercise": find_alternative_exercise_tool,
    "get_current_plan": get_current_plan_tool,
    "replace_food_in_plan": replace_food_in_plan_tool,
    "swap_meal_food": replace_food_in_plan_tool,
    "replace_exercise_in_plan": replace_exercise_in_plan_tool
}
