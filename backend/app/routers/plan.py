from fastapi import APIRouter
from app.models.schemas import GeneratePlanResponse, PlanRequest
from app.services.plan_engine import generate_plan

router = APIRouter()


@router.post("/generate-plan", response_model=GeneratePlanResponse)
async def create_plan(request: PlanRequest):
    return generate_plan(request)
