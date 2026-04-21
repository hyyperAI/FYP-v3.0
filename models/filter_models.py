from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FilterBase(BaseModel):
    filter_name: str
    keywords: Optional[List[str]] = []
    exclude_keywords: Optional[List[str]] = []
    platforms: Optional[List[str]] = []
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    budget_type: Optional[str] = None
    posted_within_hours: Optional[int] = None
    client_rank: Optional[str] = None
    client_payment_verified: Optional[bool] = None
    experience_level: Optional[List[str]] = None

class FilterCreate(FilterBase):
    user_id: str

class FilterUpdate(BaseModel):
    filter_name: Optional[str] = None
    keywords: Optional[List[str]] = None
    exclude_keywords: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    budget_type: Optional[str] = None
    posted_within_hours: Optional[int] = None
    is_active: Optional[bool] = None

class FilterResponse(FilterBase):
    filter_id: str
    user_id: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FilterListResponse(BaseModel):
    filters: List[FilterResponse]
    total: int

class MatchResultResponse(BaseModel):
    pool_entry_id: str
    filter_id: str
    user_id: str
    job_id: str
    matched_at: datetime
    match_score: Optional[float] = None
    viewed_at: Optional[datetime] = None
    status: str = "new"
    job_data: dict