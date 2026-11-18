from fastapi import APIRouter, Depends, HTTPException, status
from app.models.domain import ProfileCreate, ProfileUpdate, ProfileResponse
from app.db.mongodb import get_database
from app.api.dependencies import get_current_user
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.get("", response_model=ProfileResponse)
async def get_profile(current_user = Depends(get_current_user), db = Depends(get_database)):
    profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile_data: ProfileCreate, current_user = Depends(get_current_user), db = Depends(get_database)):
    profile_dict = profile_data.model_dump()
    profile_dict["user_id"] = str(current_user["_id"])
    
    try:
        await db.profiles.insert_one(profile_dict.copy())
        return profile_dict
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )

@router.put("", response_model=ProfileResponse)
async def update_profile(profile_data: ProfileUpdate, current_user = Depends(get_current_user), db = Depends(get_database)):
    update_data = profile_data.model_dump(exclude_unset=True)
    
    if not update_data:
        profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return profile
    
    result = await db.profiles.update_one(
        {"user_id": str(current_user["_id"])},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
    updated_profile = await db.profiles.find_one({"user_id": str(current_user["_id"])})
    return updated_profile
