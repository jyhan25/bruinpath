# BruinPath

UCLA Degree Planning Assistant — upload your transcript and DAR to get a personalized quarter-by-quarter graduation plan.

## Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 |
| PDF Parsing | PyMuPDF, pdfplumber |
| Planning | Custom rule engine |
| Deployment | Vercel (frontend) · Render/Railway/Fly.io (backend) · Supabase/Neon (DB) |

## Project Structure

```
bruinpath/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/   # health, majors, parse, audit, plan
│   │   ├── services/  # transcript_parser, dar_parser, audit_engine, plan_engine
│   │   └── models/    # Pydantic schemas
│   └── requirements.txt
├── data/              # Sample transcripts & DARs
├── docs/              # Design docs
└── docker-compose.yml
```

## API Routes

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/majors` | List available majors |
| POST | `/parse-transcript` | Parse transcript PDF |
| POST | `/parse-dar` | Parse DAR PDF |
| POST | `/audit` | Run requirements audit |
| POST | `/generate-plan` | Generate quarter plan |

## Running Locally

### With Docker Compose

```bash
docker compose up --build
```

Frontend → http://localhost:3000  
Backend → http://localhost:8000  
API Docs → http://localhost:8000/docs

### Without Docker

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit DATABASE_URL if needed
uvicorn app.main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

**Database**
```bash
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=bruinpath \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  postgres:16-alpine
```
