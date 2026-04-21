from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    user_name: Optional[str] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_status: Optional[str] = None

class UserResponse(UserBase):
    user_id: str
    is_active: bool
    subscription_status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: list
    total: int

class UserIdResponse(BaseModel):
    user_id: str
    email: str