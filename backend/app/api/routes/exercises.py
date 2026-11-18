from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import ExerciseResponse, PaginatedExerciseResponse

router = APIRouter()

def serialize_exercise(ex: dict) -> dict:
    return {
        "id": str(ex["_id"]),
        "name": ex.get("name", ""),
        "description": ex.get("description", ""),
        "category": ex.get("category", ""),
        "primary_muscle": ex.get("primary_muscle", ""),
        "secondary_muscles": ex.get("secondary_muscles", []),
        "equipment": ex.get("equipment", ""),
        "difficulty": ex.get("difficulty", "Beginner"),
        "instructions": ex.get("instructions", []),
        "sets_recommendation": ex.get("sets_recommendation"),
        "reps_recommendation": ex.get("reps_recommendation"),
        "duration_seconds": ex.get("duration_seconds"),
        "safety_notes": ex.get("safety_notes"),
        "is_active": ex.get("is_active", True),
        "created_at": ex.get("created_at"),
        "updated_at": ex.get("updated_at")
    }

@router.get("", response_model=PaginatedExerciseResponse)
async def get_exercises(
    search: Optional[str] = Query(None, description="Search by exercise name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    primary_muscle: Optional[str] = Query(None, description="Filter by primary muscle"),
    equipment: Optional[str] = Query(None, description="Filter by equipment"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    query = {"is_active": True}
    
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
        
    if category:
        query["category"] = category
        
    if primary_muscle:
        query["primary_muscle"] = primary_muscle
        
    if equipment:
        query["equipment"] = equipment
        
    if difficulty:
        query["difficulty"] = difficulty
        
    skip = (page - 1) * limit
    
    total = await db.exercises.count_documents(query)
    
    cursor = db.exercises.find(query).sort("name", 1).skip(skip).limit(limit)
    exercises = await cursor.to_list(length=limit)
    
    return {
        "items": [serialize_exercise(e) for e in exercises],
        "total": total,
        "page": page,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(exercise_id):
        raise HTTPException(status_code=400, detail="Invalid exercise ID")
        
    exercise = await db.exercises.find_one({"_id": ObjectId(exercise_id), "is_active": True})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
        
    return serialize_exercise(exercise)
