from fastapi import APIRouter
from app.models.schemas import AuditRequest, AuditResponse
from app.services.audit_engine import run_audit

router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
async def audit(request: AuditRequest):
    return run_audit(request)
