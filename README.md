# FYP Job Matching Backend

AI-powered job matching system API built with FastAPI and Supabase.

## Features

- **Job Management** - Browse and search job listings from multiple platforms
- **Smart Filters** - Create custom filters with keywords, budget, skills
- **Auto Matching** - Intelligent job-filter matching engine
- **Proposal Templates** - Save and manage application templates
- **User Management** - Profile and preferences management

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone <your-repo>
cd fyp-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
```

### 3. Run Server

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

### 4. Access API

- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/jobs/` | Get all jobs |
| GET | `/jobs/{job_id}` | Get job by ID |
| POST | `/jobs/` | Create job |
| POST | `/jobs/bulk` | Create multiple jobs |
| PUT | `/jobs/{job_id}` | Update job |
| DELETE | `/jobs/{job_id}` | Delete job |
| GET | `/jobs/recent` | Get recent jobs |

### Filters
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/filters/` | Get all filters |
| GET | `/filters/{filter_id}` | Get filter by ID |
| POST | `/filters/` | Create filter |
| PUT | `/filters/{filter_id}` | Update filter |
| DELETE | `/filters/{filter_id}` | Delete filter |

### Matching
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/matching/trigger` | Trigger matching engine |
| GET | `/matching/results/{filter_id}` | Get matched jobs |
| POST | `/matching/results/{filter_id}/mark-viewed` | Mark as viewed |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | Get all users |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/id-from-email/{email}` | Get user_id by email |
| POST | `/users/` | Create user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Proposals
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/proposals/` | Get all proposals |
| GET | `/proposals/{proposal_id}` | Get proposal by ID |
| POST | `/proposals/` | Create proposal |
| PUT | `/proposals/{proposal_id}` | Update proposal |
| DELETE | `/proposals/{proposal_id}` | Delete proposal |

## Example Usage

### Create a Filter
```bash
curl -X POST http://localhost:8000/filters/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid",
    "filter_name": "Python Jobs",
    "keywords": ["python", "fastapi"],
    "min_budget": 500,
    "max_budget": 2000
  }'
```

### Trigger Matching
```bash
curl -X POST http://localhost:8000/matching/trigger
```

### Get Matched Jobs
```bash
curl http://localhost:8000/matching/results/{filter_id}
```

## Database Schema

```
users ─────┐
           │
filters ───┼──> filter_pools ──> proposals
           │
data_pool ─┘
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deployment
1. Set up environment variables
2. Run: `gunicorn main:app --workers 4 --bind 0.0.0.0:8000`
3. Configure NGINX reverse proxy
4. Set up SSL certificate

## Project Structure

```
fyp-backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Environment configuration
├── requirements.txt       # Python dependencies
├── routers/              # API route modules
│   ├── jobs.py          # Job endpoints
│   ├── filters.py       # Filter endpoints
│   ├── matching.py      # Matching endpoints
│   ├── users.py         # User endpoints
│   └── proposals.py    # Proposal endpoints
├── models/               # Pydantic data models
│   ├── job_models.py
│   ├── filter_models.py
│   ├── user_models.py
│   └── proposal_models.py
└── services/            # Business logic
    ├── supabase_client.py
    └── data_operations.py
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase API key | Yes |

## License

MIT License - See LICENSE file for details.