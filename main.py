from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routers import jobs, filters, matching, users, proposals, ai

app = FastAPI(
    title="FYP Job Matching API",
    description="""
## API Overview

AI-powered job matching system that helps users find relevant job opportunities based on their preferences.

## Features

- **Job Management**: Browse, search, and filter job listings from multiple platforms
- **Filter System**: Create custom filters with keywords, budget ranges, skills, and more
- **Matching Engine**: Automatic job-filter matching with real-time results
- **Proposal Templates**: Save and manage proposal templates for job applications
- **User Management**: User profile and preferences management

## Base URL

- Local Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

Currently using Supabase authentication. Include your auth token in headers:
```
Authorization: Bearer <your-token>
```

## Rate Limits

No rate limits for development. Configure in production as needed.

## Support

For questions or issues, check the project documentation.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(filters.router)
app.include_router(matching.router)
app.include_router(users.router)
app.include_router(proposals.router)
app.include_router(ai.router)

@app.get("/", tags=["Info"])
async def root():
    """
    API Root Endpoint
    
    Returns basic API information and status.
    
    **Response:**
    - message: API greeting message
    - status: API running status
    """
    return {
        "message": "FYP Job Matching Backend API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Info"])
async def health_check():
    """
    Health Check Endpoint
    
    Returns API health status. Useful for monitoring and load balancers.
    
    **Response:**
    - status: "healthy" if API is running
    """
    return {"status": "healthy"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="FYP Job Matching API",
        version="1.0.0",
        description="""
## API Overview

AI-powered job matching system that helps users find relevant job opportunities based on their preferences.

## Features

- **Job Management**: Browse, search, and filter job listings from multiple platforms
- **Filter System**: Create custom filters with keywords, budget ranges, skills, and more
- **Matching Engine**: Automatic job-filter matching with real-time results
- **Proposal Templates**: Save and manage proposal templates for job applications
- **User Management**: User profile and preferences management
        """,
        routes=app.routes,
    )
    
    openapi_schema["info"]["contact"] = {
        "name": "FYP Project",
        "description": "AI-Powered Job Matching System"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi