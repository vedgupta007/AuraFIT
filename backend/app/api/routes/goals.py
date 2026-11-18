from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter()

def serialize_goal(goal: dict) -> dict:
    return {
        "id": str(goal["_id"]),
        "user_id": str(goal["user_id"]),
        "goal_type": goal["goal_type"],
        "title": goal["title"],
        "description": goal.get("description"),
        "target_value": goal.get("target_value"),
        "current_value": goal.get("current_value"),
        "start_date": goal["start_date"],
        "target_date": goal.get("target_date"),
        "status": goal["status"],
        "created_at": goal["created_at"],
        "updated_at": goal["updated_at"]
    }

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(goal: GoalCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    goal_dict = goal.model_dump()
    goal_dict["user_id"] = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    goal_dict["created_at"] = now
    goal_dict["updated_at"] = now
    
    result = await db.goals.insert_one(goal_dict)
    goal_dict["_id"] = result.inserted_id
    
    return serialize_goal(goal_dict)

@router.get("/", response_model=List[GoalResponse])
async def get_goals(status: Optional[str] = None, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    query = {"user_id": str(current_user["_id"])}
    if status:
        query["status"] = status
        
    cursor = db.goals.find(query).sort("created_at", -1)
    goals = await cursor.to_list(length=100)
    return [serialize_goal(g) for g in goals]

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: str, goal_update: GoalUpdate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(goal_id):
        raise HTTPException(status_code=400, detail="Invalid goal ID format")
        
    update_data = {k: v for k, v in goal_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await db.goals.find_one_and_update(
        {"_id": ObjectId(goal_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    return serialize_goal(result)

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(goal_id):
        raise HTTPException(status_code=400, detail="Invalid goal ID format")
        
    result = await db.goals.delete_one({"_id": ObjectId(goal_id), "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    return None