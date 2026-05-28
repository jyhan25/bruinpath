from fastapi import APIRouter
from app.models.schemas import Major

router = APIRouter()

# Stub data — replace with DB query once schema is set up
_MAJORS: list[Major] = [
    Major(id="cs", name="Computer Science", department="Engineering", total_units=180,
          description="B.S. in Computer Science"),
    Major(id="math", name="Mathematics", department="Mathematics", total_units=180,
          description="B.S. in Mathematics"),
    Major(id="econ", name="Economics", department="Social Sciences", total_units=180,
          description="B.A. in Economics"),
    Major(id="stats", name="Statistics", department="Mathematics", total_units=180,
          description="B.S. in Statistics"),
]


@router.get("/majors", response_model=list[Major])
async def list_majors():
    return _MAJORS
