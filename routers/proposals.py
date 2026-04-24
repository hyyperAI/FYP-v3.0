from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.proposal_models import (
    ProposalCreate, 
    ProposalUpdate, 
    ProposalResponse, 
    ProposalListResponse
)
from services import data_operations

router = APIRouter(prefix="/proposals", tags=["Proposals"])

@router.get("/", response_model=ProposalListResponse)
async def get_proposals(
    user_id: Optional[str] = Query(None),
    template: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    proposals = data_operations.get_proposals(
        user_id=user_id, 
        template=template, 
        limit=limit
    )
    return ProposalListResponse(proposals=proposals, total=len(proposals))

@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(proposal_id: str):
    proposal = data_operations.get_proposal_by_id(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return ProposalResponse(**proposal)

@router.post("/", response_model=ProposalResponse)
async def create_proposal(proposal: ProposalCreate):
    proposal_data = proposal.model_dump()
    created_proposal = data_operations.create_proposal(proposal_data)
    return ProposalResponse(**created_proposal)

@router.put("/{proposal_id}", response_model=ProposalResponse)
async def update_proposal(proposal_id: str, proposal: ProposalUpdate):
    existing = data_operations.get_proposal_by_id(proposal_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    proposal_data = proposal.model_dump(exclude_unset=True)
    updated_proposal = data_operations.update_proposal(proposal_id, proposal_data)
    return ProposalResponse(**updated_proposal)

@router.delete("/{proposal_id}")
async def delete_proposal(proposal_id: str):
    existing = data_operations.get_proposal_by_id(proposal_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    data_operations.delete_proposal(proposal_id)
    return {"message": "Proposal deleted successfully"}