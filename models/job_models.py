from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str
    platform: Optional[str] = None
    skills: Optional[List[str]] = []
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    budget_type: Optional[str] = None
    budget_display: Optional[str] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    duration: Optional[str] = None
    engagement: Optional[str] = None
    categories: Optional[List[str]] = []
    client_rating: Optional[float] = None
    client_country_name: Optional[str] = None
    platform_url: Optional[str] = None

class JobCreate(JobBase):
    external_job_id: Optional[str] = None
    published_at: Optional[datetime] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None

class JobResponse(BaseModel):
    job_id: str
    external_job_id: Optional[str] = None
    platform: Optional[str] = None
    title: str
    description: str
    skills: Optional[List[str]] = []
    budget_type: Optional[str] = None
    budget_display: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    duration: Optional[str] = None
    engagement: Optional[str] = None
    categories: Optional[List[str]] = []
    client_rating: Optional[float] = None
    client_country_name: Optional[str] = None
    platform_url: Optional[str] = None
    published_at: Optional[datetime] = None
    ingested_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int