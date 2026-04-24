#!/usr/bin/env python3
"""
Add Sample Jobs to Database
Run: python add_sample_jobs.py
"""
from services.supabase_client import get_supabase_client

s = get_supabase_client()

jobs = [
    {
        "title": "Python Developer - Web App",
        "description": "Looking for experienced Python developer for web application development",
        "platform": "Upwork.com",
        "external_job_id": "UPW-111111",
        "skills": ["python", "fastapi", "react"],
        "budget_min": 800.0,
        "budget_max": 1200.0,
        "budget_type": "fixed",
        "budget_display": "$800 - $1200 USD",
        "experience_level": "Expert",
        "published_at": "2026-04-21T10:00:00+00:00",
        "vollna_redirect_url": "https://example.com/job/UPW-111111",
        "platform_url": "https://upwork.com/jobs/UPW-111111",
        "client_payment_verified": True,
        "client_rating": 4.5,
        "client_country_name": "USA",
        "raw_payload": {"id": "UPW-111111", "source": "test"}
    },
    {
        "title": "Java Backend Engineer",
        "description": "Need Java backend developer for enterprise system",
        "platform": "LinkedIn",
        "external_job_id": "LNK-222222",
        "skills": ["java", "spring", "microservices"],
        "budget_min": 600.0,
        "budget_max": 900.0,
        "budget_type": "hourly",
        "budget_display": "$60/hr",
        "experience_level": "Intermediate",
        "published_at": "2026-04-21T10:00:00+00:00",
        "vollna_redirect_url": "https://example.com/job/LNK-222222",
        "platform_url": "https://linkedin.com/jobs/LNK-222222",
        "client_payment_verified": True,
        "client_rating": 4.2,
        "client_country_name": "UK",
        "raw_payload": {"id": "LNK-222222", "source": "test"}
    },
    {
        "title": "Full Stack Developer Needed",
        "description": "Looking for full stack developer with React and Node.js experience",
        "platform": "Indeed",
        "external_job_id": "IND-333333",
        "skills": ["javascript", "react", "node.js", "mongodb"],
        "budget_min": 1000.0,
        "budget_max": 1500.0,
        "budget_type": "fixed",
        "budget_display": "$1000 - $1500 USD",
        "experience_level": "Expert",
        "published_at": "2026-04-21T10:00:00+00:00",
        "vollna_redirect_url": "https://example.com/job/IND-333333",
        "platform_url": "https://indeed.com/jobs/IND-333333",
        "client_payment_verified": True,
        "client_rating": 4.8,
        "client_country_name": "Canada",
        "raw_payload": {"id": "IND-333333", "source": "test"}
    }
]

print("Adding sample jobs to database...")
print("=" * 50)

for job in jobs:
    result = s.table("data_pool").insert(job).execute()
    print(f"Added: {job['title']}")

print("=" * 50)
print(f"Total jobs added: {len(jobs)}")
print("\nTest API: curl http://localhost:8000/jobs/")
