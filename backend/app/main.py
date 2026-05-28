from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import audit, health, majors, parse, plan

app = FastAPI(title="BruinPath API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(majors.router)
app.include_router(parse.router)
app.include_router(audit.router)
app.include_router(plan.router)
