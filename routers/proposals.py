from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.proposal_models import (
    ApplicationCreate, 
    ApplicationUpdate, 
    ApplicationResponse, 
    ApplicationListResponse,
    MarkResponseRequest
)
from services import data_operations

router = APIRouter(prefix="/proposals", tags=["Proposals"])

@router.get("/", response_model=ApplicationListResponse)
async def get_applications(
    user_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    applications = data_operations.get_applications(
        user_id=user_id, 
        status=status, 
        limit=limit
    )
    return ApplicationListResponse(applications=applications, total=len(applications))

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: str):
    application = data_operations.get_application_by_id(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return ApplicationResponse(**application)

@router.get("/pool/{pool_entry_id}")
async def get_application_by_pool(pool_entry_id: str, user_id: Optional[str] = None):
    application = data_operations.get_application_by_pool_entry(pool_entry_id, user_id)
    if not application:
        raise HTTPException(status_code=404, detail="No application found for this pool entry")
    return ApplicationResponse(**application)

@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate):
    existing = data_operations.get_application_by_pool_entry(
        application.pool_entry_id, 
        application.user_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Application already exists for this job")
    
    application_data = application.model_dump()
    created_application = data_operations.create_application(application_data)
    return ApplicationResponse(**created_application)

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(application_id: str, application: ApplicationUpdate):
    existing = data_operations.get_application_by_id(application_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application_data = application.model_dump(exclude_unset=True)
    updated_application = data_operations.update_application(application_id, application_data)
    return ApplicationResponse(**updated_application)

@router.delete("/{application_id}")
async def delete_application(application_id: str):
    existing = data_operations.get_application_by_id(application_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Application not found")
    
    data_operations.delete_application(application_id)
    return {"message": "Application deleted successfully"}

@router.post("/{application_id}/apply")
async def mark_application_applied(application_id: str):
    existing = data_operations.get_application_by_id(application_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if existing.get("status") == "applied":
        raise HTTPException(status_code=400, detail="Application already applied")
    
    result = data_operations.mark_application_applied(application_id)
    return {
        "message": "Application marked as applied",
        "application_id": result["application_id"],
        "status": result["status"],
        "applied_at": result["applied_at"]
    }

@router.post("/{application_id}/response")
async def mark_application_response(application_id: str, payload: MarkResponseRequest):
    existing = data_operations.get_application_by_id(application_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Application not found")
    
    result = data_operations.mark_application_response(application_id, payload.received)
    return {
        "message": f"Response marked as {'received' if payload.received else 'not received'}",
        "application_id": result["application_id"],
        "response_received": result["response_received"]
    }