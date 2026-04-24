from services.supabase_client import get_supabase_client
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

def get_jobs(limit: int = 100, offset: int = 0, platform: Optional[str] = None) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("data_pool").select("*").range(offset, offset + limit - 1)
    
    if platform:
        query = query.eq("platform", platform)
    
    result = query.execute()
    return result.data

def get_job_by_id(job_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("data_pool").select("*").eq("job_id", job_id).execute()
    return result.data[0] if result.data else None

def create_job(job_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("data_pool").insert(job_data).execute()
    return result.data[0]

def create_jobs_bulk(jobs_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("data_pool").insert(jobs_data).execute()
    return result.data

def update_job(job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("data_pool").update(job_data).eq("job_id", job_id).execute()
    return result.data[0]

def delete_job(job_id: str) -> bool:
    supabase = get_supabase_client()
    supabase.table("data_pool").delete().eq("job_id", job_id).execute()
    return True

def get_recent_jobs(minutes: int = 60, limit: int = 100) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    result = supabase.table("data_pool").select("*").gte("published_at", time_threshold.isoformat()).limit(limit).execute()
    return result.data

def get_filters(user_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("filters").select("*").limit(limit)
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    result = query.execute()
    return result.data

def get_filter_by_id(filter_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("filters").select("*").eq("filter_id", filter_id).execute()
    return result.data[0] if result.data else None

def create_filter(filter_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("filters").insert(filter_data).execute()
    return result.data[0]

def update_filter(filter_id: str, filter_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("filters").update(filter_data).eq("filter_id", filter_id).execute()
    try:
        trigger_matching(filter_id)
    except Exception:
        pass
    return result.data[0]

def delete_filter(filter_id: str) -> bool:
    supabase = get_supabase_client()
    supabase.table("filters").delete().eq("filter_id", filter_id).execute()
    return True

def get_filter_matches(filter_id: str, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("filter_pools").select("*, data_pool:*").eq("filter_id", filter_id).limit(limit)
    
    if status:
        query = query.eq("status", status)
    
    result = query.execute()
    return result.data

def trigger_matching(filter_id: Optional[str] = None) -> Dict[str, Any]:
    supabase = get_supabase_client()
    
    if filter_id:
        result = supabase.rpc("match_jobs_to_filters", {"filter_id_param": filter_id}).execute()
    else:
        result = supabase.rpc("match_jobs_to_filters").execute()
    
    return {"status": "success", "matches_created": len(result.data) if result.data else 0}

def mark_match_viewed(pool_entry_id: str) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("filter_pools").update({"viewed_at": datetime.now().isoformat()}).eq("pool_entry_id", pool_entry_id).execute()
    return result.data[0]

def get_users(limit: int = 100, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("users").select("*").limit(limit)
    
    if is_active is not None:
        query = query.eq("is_active", is_active)
    
    result = query.execute()
    return result.data

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("users").select("*").eq("user_id", user_id).execute()
    return result.data[0] if result.data else None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("users").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None

def get_user_id_by_email(email: str) -> Optional[str]:
    supabase = get_supabase_client()
    result = supabase.table("users").select("user_id").eq("email", email).execute()
    return result.data[0]["user_id"] if result.data else None

def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("users").insert(user_data).execute()
    return result.data[0]

def update_user(user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("users").update(user_data).eq("user_id", user_id).execute()
    return result.data[0]

def delete_user(user_id: str) -> bool:
    supabase = get_supabase_client()
    supabase.table("users").delete().eq("user_id", user_id).execute()
    return True

def get_applications(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("applications").select("*").limit(limit)
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    if status:
        query = query.eq("status", status)
    
    result = query.execute()
    return result.data

def get_application_by_id(application_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("applications").select("*").eq("application_id", application_id).execute()
    return result.data[0] if result.data else None

def get_application_by_pool_entry(pool_entry_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("applications").select("*").eq("pool_entry_id", pool_entry_id)
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    result = query.execute()
    return result.data[0] if result.data else None

def create_application(application_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("applications").insert(application_data).execute()
    return result.data[0]

def update_application(application_id: str, application_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("applications").update(application_data).eq("application_id", application_id).execute()
    return result.data[0]

def delete_application(application_id: str) -> bool:
    supabase = get_supabase_client()
    supabase.table("applications").delete().eq("application_id", application_id).execute()
    return True

def mark_application_applied(application_id: str) -> Dict[str, Any]:
    supabase = get_supabase_client()
    applied_time = datetime.now().isoformat()
    result = supabase.table("applications").update({
        "status": "applied",
        "applied_at": applied_time
    }).eq("application_id", application_id).execute()
    return result.data[0]

def mark_application_response(application_id: str, received: bool) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("applications").update({
        "response_received": received
    }).eq("application_id", application_id).execute()
    return result.data[0]

def get_proposals(
    user_id: Optional[str] = None,
    template: Optional[bool] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    query = supabase.table("proposals").select("*").limit(limit)
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    if template is not None:
        query = query.eq("template", str(template).lower())
    
    result = query.execute()
    return result.data

def get_proposal_by_id(proposal_id: str) -> Optional[Dict[str, Any]]:
    supabase = get_supabase_client()
    result = supabase.table("proposals").select("*").eq("proposal_id", proposal_id).execute()
    return result.data[0] if result.data else None

def create_proposal(proposal_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("proposals").insert(proposal_data).execute()
    return result.data[0]

def update_proposal(proposal_id: str, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
    supabase = get_supabase_client()
    result = supabase.table("proposals").update(proposal_data).eq("proposal_id", proposal_id).execute()
    return result.data[0]

def delete_proposal(proposal_id: str) -> bool:
    supabase = get_supabase_client()
    supabase.table("proposals").delete().eq("proposal_id", proposal_id).execute()
    return True
