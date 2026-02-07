from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import timedelta
from src.core.security import create_access_token, verify_password, hash_password
from src.core.config import settings
import uuid

# Simple in-memory user storage for testing
users_db: Dict[str, dict] = {}

# Define request/response models
class UserCreateRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserDetailResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreateRequest):
    # Check if user already exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Create new user
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "name": user_data.name
    }
    
    users_db[user_id] = user
    
    return UserResponse(id=user["id"], email=user["email"], name=user["name"])


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLoginRequest):
    # Find user by email
    user = None
    for u in users_db.values():
        if u["email"] == user_data.email:
            user = u
            break
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")


# Import the get_current_user dependency from auth service
from src.services.auth import get_current_user

@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_from_token(current_user_id: str = Depends(get_current_user)):
    user = users_db.get(current_user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserDetailResponse(id=user["id"], email=user["email"], name=user["name"])