from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import FoodResponse, PaginatedFoodResponse

router = APIRouter()

def serialize_food(food: dict) -> dict:
    return {
        "id": str(food["_id"]),
        "name": food.get("name", ""),
        "category": food.get("category", ""),
        "serving_size": food.get("serving_size", 0.0),
        "serving_unit": food.get("serving_unit", ""),
        "calories": food.get("calories", 0.0),
        "protein": food.get("protein", 0.0),
        "carbohydrates": food.get("carbohydrates", 0.0),
        "fat": food.get("fat", 0.0),
        "fiber": food.get("fiber", 0.0),
        "diet_types": food.get("diet_types", []),
        "allergens": food.get("allergens", []),
        "is_vegetarian": food.get("is_vegetarian", False),
        "is_vegan": food.get("is_vegan", False),
        "is_eggetarian": food.get("is_eggetarian", False),
        "is_active": food.get("is_active", True),
        "created_at": food.get("created_at"),
        "updated_at": food.get("updated_at")
    }

@router.get("", response_model=PaginatedFoodResponse)
async def get_foods(
    search: Optional[str] = Query(None, description="Search by food name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_vegetarian: Optional[bool] = None,
    is_vegan: Optional[bool] = None,
    is_eggetarian: Optional[bool] = None,
    min_protein: Optional[float] = Query(None, ge=0),
    max_calories: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    query = {"is_active": True}
    
    if search:
        # Case-insensitive regex search
        query["name"] = {"$regex": search, "$options": "i"}
        
    if category:
        query["category"] = category
        
    if is_vegetarian is not None:
        query["is_vegetarian"] = is_vegetarian
        
    if is_vegan is not None:
        query["is_vegan"] = is_vegan
        
    if is_eggetarian is not None:
        query["is_eggetarian"] = is_eggetarian
        
    if min_protein is not None:
        query["protein"] = {"$gte": min_protein}
        
    if max_calories is not None:
        query["calories"] = {"$lte": max_calories}
        
    skip = (page - 1) * limit
    
    # Count total documents matching query
    total = await db.foods.count_documents(query)
    
    # Fetch paginated data
    cursor = db.foods.find(query).sort("name", 1).skip(skip).limit(limit)
    foods = await cursor.to_list(length=limit)
    
    return {
        "items": [serialize_food(f) for f in foods],
        "total": total,
        "page": page,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(food_id):
        raise HTTPException(status_code=400, detail="Invalid food ID")
        
    food = await db.foods.find_one({"_id": ObjectId(food_id), "is_active": True})
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
        
    return serialize_food(food)
