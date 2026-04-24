from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProposalBase(BaseModel):
    user_id: str
    proposal_name: str
    title: str
    instructions: Optional[str] = None
    context: Optional[str] = None
    template: bool = False
    ai_model: Optional[str] = "gpt-4"
    hourly_rate: Optional[float] = 0.0
    fixed_rate: Optional[float] = 0.0

class ProposalCreate(ProposalBase):
    pass

class ProposalUpdate(BaseModel):
    proposal_name: Optional[str] = None
    title: Optional[str] = None
    instructions: Optional[str] = None
    context: Optional[str] = None
    template: Optional[bool] = None
    ai_model: Optional[str] = None
    hourly_rate: Optional[float] = None
    fixed_rate: Optional[float] = None

class ProposalResponse(ProposalBase):
    proposal_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProposalListResponse(BaseModel):
    proposals: list
    total: int