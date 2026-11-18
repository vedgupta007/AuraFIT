from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import WorkoutCreate, WorkoutUpdate, WorkoutResponse

router = APIRouter()

def serialize_workout(workout: dict) -> dict:
    return {
        "id": str(workout["_id"]),
        "user_id": str(workout["user_id"]),
        "title": workout["title"],
        "started_at": workout["started_at"],
        "ended_at": workout.get("ended_at"),
        "notes": workout.get("notes"),
        "exercises": workout.get("exercises", []),
        "created_at": workout["created_at"],
        "updated_at": workout["updated_at"]
    }

@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout: WorkoutCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    workout_dict = workout.model_dump()
    workout_dict["user_id"] = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    workout_dict["created_at"] = now
    workout_dict["updated_at"] = now
    
    result = await db.workouts.insert_one(workout_dict)
    workout_dict["_id"] = result.inserted_id
    
    return serialize_workout(workout_dict)

@router.get("/", response_model=List[WorkoutResponse])
async def get_workouts(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    user_id = str(current_user["_id"])
    cursor = db.workouts.find({"user_id": user_id}).sort("started_at", -1).skip(skip).limit(limit)
    workouts = await cursor.to_list(length=limit)
    return [serialize_workout(w) for w in workouts]

@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID format")
        
    workout = await db.workouts.find_one({"_id": ObjectId(workout_id), "user_id": str(current_user["_id"])})
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
        
    return serialize_workout(workout)

@router.put("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(
    workout_id: str,
    workout_update: WorkoutUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID format")
        
    update_data = {k: v for k, v in workout_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await db.workouts.find_one_and_update(
        {"_id": ObjectId(workout_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Workout not found")
        
    return serialize_workout(result)

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID format")
        
    result = await db.workouts.delete_one({"_id": ObjectId(workout_id), "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")
        
    return None