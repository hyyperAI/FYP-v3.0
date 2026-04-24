from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.job_models import JobCreate, JobUpdate, JobResponse, JobListResponse
from services import data_operations

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/", response_model=JobListResponse)
async def get_jobs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    platform: Optional[str] = None
):
    jobs = data_operations.get_jobs(limit=limit, offset=offset, platform=platform)
    return JobListResponse(jobs=[JobResponse(**job) for job in jobs], total=len(jobs))

@router.get("/recent", response_model=List[JobResponse])
async def get_recent_jobs(
    minutes: int = Query(60, ge=1, le=10080),
    limit: int = Query(100, ge=1, le=1000)
):
    jobs = data_operations.get_recent_jobs(minutes=minutes, limit=limit)
    return [JobResponse(**job) for job in jobs]

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    job = data_operations.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate):
    job_data = job.model_dump(exclude_unset=True)
    created_job = data_operations.create_job(job_data)
    return JobResponse(**created_job)

@router.post("/bulk", response_model=List[JobResponse])
async def create_jobs_bulk(jobs: List[JobCreate]):
    jobs_data = [job.model_dump(exclude_unset=True) for job in jobs]
    created_jobs = data_operations.create_jobs_bulk(jobs_data)
    return [JobResponse(**job) for job in created_jobs]

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(job_id: str, job: JobUpdate):
    existing_job = data_operations.get_job_by_id(job_id)
    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = job.model_dump(exclude_unset=True)
    updated_job = data_operations.update_job(job_id, job_data)
    return JobResponse(**updated_job)

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    existing_job = data_operations.get_job_by_id(job_id)
    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    data_operations.delete_job(job_id)
    return {"message": "Job deleted successfully"}