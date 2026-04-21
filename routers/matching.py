from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.filter_models import MatchResultResponse
from services import data_operations

router = APIRouter(prefix="/matching", tags=["Matching"])

@router.post("/trigger")
async def trigger_matching(filter_id: Optional[str] = None):
    try:
        result = data_operations.trigger_matching(filter_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@router.get("/results/{filter_id}", response_model=List[dict])
async def get_filter_matches(
    filter_id: str,
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    filter_data = data_operations.get_filter_by_id(filter_id)
    if not filter_data:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    matches = data_operations.get_filter_matches(filter_id, status=status, limit=limit)
    return matches

@router.post("/results/{filter_id}/mark-viewed")
async def mark_match_viewed(filter_id: str, pool_entry_id: str):
    filter_data = data_operations.get_filter_by_id(filter_id)
    if not filter_data:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    try:
        result = data_operations.mark_match_viewed(pool_entry_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark as viewed: {str(e)}")