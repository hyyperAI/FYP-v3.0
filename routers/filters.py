from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.filter_models import FilterCreate, FilterUpdate, FilterResponse, FilterListResponse
from services import data_operations

router = APIRouter(prefix="/filters", tags=["Filters"])

@router.get("/", response_model=FilterListResponse)
async def get_filters(
    user_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    filters = data_operations.get_filters(user_id=user_id, limit=limit)
    return FilterListResponse(filters=[FilterResponse(**f) for f in filters], total=len(filters))

@router.get("/{filter_id}", response_model=FilterResponse)
async def get_filter(filter_id: str):
    filter_data = data_operations.get_filter_by_id(filter_id)
    if not filter_data:
        raise HTTPException(status_code=404, detail="Filter not found")
    return FilterResponse(**filter_data)

@router.post("/", response_model=FilterResponse)
async def create_filter(filter: FilterCreate):
    filter_data = filter.model_dump()
    created_filter = data_operations.create_filter(filter_data)
    return FilterResponse(**created_filter)

@router.put("/{filter_id}", response_model=FilterResponse)
async def update_filter(filter_id: str, filter: FilterUpdate):
    existing_filter = data_operations.get_filter_by_id(filter_id)
    if not existing_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    filter_data = filter.model_dump(exclude_unset=True)
    updated_filter = data_operations.update_filter(filter_id, filter_data)
    return FilterResponse(**updated_filter)

@router.delete("/{filter_id}")
async def delete_filter(filter_id: str):
    existing_filter = data_operations.get_filter_by_id(filter_id)
    if not existing_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    data_operations.delete_filter(filter_id)
    return {"message": "Filter deleted successfully"}