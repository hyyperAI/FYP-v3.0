from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.user_models import UserCreate, UserUpdate, UserResponse, UserListResponse, UserIdResponse
from services import data_operations

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UserListResponse)
async def get_users(
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None
):
    users = data_operations.get_users(limit=limit, is_active=is_active)
    return UserListResponse(users=users, total=len(users))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = data_operations.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    user = data_operations.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)

@router.get("/id-from-email/{email}", response_model=UserIdResponse)
async def get_user_id_by_email(email: str):
    user_id = data_operations.get_user_id_by_email(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return UserIdResponse(user_id=user_id, email=email)

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing = data_operations.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = user.model_dump()
    created_user = data_operations.create_user(user_data)
    return UserResponse(**created_user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    existing_user = data_operations.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.model_dump(exclude_unset=True)
    updated_user = data_operations.update_user(user_id, user_data)
    return UserResponse(**updated_user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    existing_user = data_operations.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    data_operations.delete_user(user_id)
    return {"message": "User deleted successfully"}