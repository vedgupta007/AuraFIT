from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.models.domain import UserCreate, UserLogin, UserResponse, TokenResponse
from app.db.mongodb import get_database
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, verify_token
from app.api.dependencies import get_current_user
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, response: Response, db = Depends(get_database)):
    normalized_email = user.email.lower().strip()
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "email": normalized_email,
        "password_hash": hashed_password,
        "role": "user",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    try:
        result = await db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, response: Response, db = Depends(get_database)):
    normalized_email = user_credentials.email.lower().strip()
    user = await db.users.find_one({"email": normalized_email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = str(user["_id"])
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request, response: Response, db = Depends(get_database)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
        
    payload = verify_token(refresh_token, "refresh")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    user_id = payload.get("sub")
    
    # Optional: verify user still exists in DB
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response, current_user = Depends(get_current_user)):
    response.delete_cookie(key="refresh_token")
    return {"status": "success", "message": "Logged out"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"],
        "created_at": current_user["created_at"]
    }

