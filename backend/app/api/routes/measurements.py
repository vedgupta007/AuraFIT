from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from app.models.domain import MeasurementCreate, MeasurementUpdate, MeasurementResponse

router = APIRouter()

def serialize_measurement(m: dict) -> dict:
    return {
        "id": str(m["_id"]),
        "user_id": str(m["user_id"]),
        "date": m["date"],
        "weight_kg": m.get("weight_kg"),
        "body_fat_percent": m.get("body_fat_percent"),
        "waist_cm": m.get("waist_cm"),
        "chest_cm": m.get("chest_cm"),
        "arms_cm": m.get("arms_cm"),
        "thighs_cm": m.get("thighs_cm"),
        "hips_cm": m.get("hips_cm"),
        "neck_cm": m.get("neck_cm"),
        "notes": m.get("notes"),
        "created_at": m["created_at"],
        "updated_at": m["updated_at"]
    }

@router.post("/", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement(measurement: MeasurementCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    m_dict = measurement.model_dump()
    m_dict["user_id"] = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    m_dict["created_at"] = now
    m_dict["updated_at"] = now
    
    result = await db.measurements.insert_one(m_dict)
    m_dict["_id"] = result.inserted_id
    
    return serialize_measurement(m_dict)

@router.get("/", response_model=List[MeasurementResponse])
async def get_measurements(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    cursor = db.measurements.find({"user_id": str(current_user["_id"])}).sort("date", -1)
    measurements = await cursor.to_list(length=365)
    return [serialize_measurement(m) for m in measurements]

@router.put("/{measurement_id}", response_model=MeasurementResponse)
async def update_measurement(measurement_id: str, measurement_update: MeasurementUpdate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(measurement_id):
        raise HTTPException(status_code=400, detail="Invalid measurement ID format")
        
    update_data = {k: v for k, v in measurement_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await db.measurements.find_one_and_update(
        {"_id": ObjectId(measurement_id), "user_id": str(current_user["_id"])},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Measurement not found")
        
    return serialize_measurement(result)

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(measurement_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(measurement_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    result = await db.measurements.delete_one({"_id": ObjectId(measurement_id), "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Measurement not found")
        
    return None