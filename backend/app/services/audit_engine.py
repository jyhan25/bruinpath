from app.models.schemas import (
    AuditRequest,
    AuditResponse,
    AuditResult,
    DARRequirement,
    TranscriptCourse,
)


def _courses_by_id(courses: list[TranscriptCourse]) -> dict[str, TranscriptCourse]:
    return {c.course_id.strip().upper(): c for c in courses}


def _passing_grade(grade: str) -> bool:
    return grade not in {"F", "NP", "W", "I"}


def _audit_requirement(
    req: DARRequirement,
    completed_course_ids: set[str],
) -> AuditResult:
    applied = req.units_applied
    required = req.units_required

    if req.status == "complete" or applied >= required:
        return AuditResult(requirement=req.requirement, status="complete")

    missing = [c for c in req.courses if c.upper() not in completed_course_ids]
    if applied > 0:
        return AuditResult(
            requirement=req.requirement,
            status="in_progress",
            missing_courses=missing,
            notes=f"{applied}/{required} units applied",
        )

    return AuditResult(
        requirement=req.requirement,
        status="incomplete",
        missing_courses=missing,
        notes=f"0/{required} units applied",
    )


def run_audit(request: AuditRequest) -> AuditResponse:
    completed_ids: set[str] = {
        c.course_id.strip().upper()
        for c in request.transcript.courses
        if _passing_grade(c.grade)
    }

    passed: list[AuditResult] = []
    pending: list[AuditResult] = []
    failed: list[AuditResult] = []

    for req in request.dar.requirements:
        result = _audit_requirement(req, completed_ids)
        if result.status == "complete":
            passed.append(result)
        elif result.status == "in_progress":
            pending.append(result)
        else:
            failed.append(result)

    total = len(request.dar.requirements)
    completion = (len(passed) / total * 100) if total else 0.0

    return AuditResponse(
        major=request.dar.major or request.transcript.major,
        passed=passed,
        pending=pending,
        failed=failed,
        completion_percentage=round(completion, 1),
    )
