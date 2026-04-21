from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    pool_entry_id: str
    user_id: str
    status: str = "draft"
    cover_letter: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None
    response_received: Optional[bool] = None
    applied_at: Optional[datetime] = None

class ApplicationResponse(ApplicationBase):
    application_id: str
    applied_at: Optional[datetime] = None
    response_received: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApplicationListResponse(BaseModel):
    applications: list
    total: int

class MarkAppliedResponse(BaseModel):
    application_id: str
    status: str
    applied_at: datetime

class MarkResponseRequest(BaseModel):
    received: bool