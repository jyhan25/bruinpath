from app.models.schemas import (
    GeneratePlanResponse,
    PlanRequest,
    PlannedCourse,
    QuarterPlan,
)

QUARTER_ORDER = ["Winter", "Spring", "Summer", "Fall"]


def _next_term(term: str) -> str:
    """Advance one quarter."""
    parts = term.split()
    if len(parts) != 2:
        return term
    season, year = parts[0], int(parts[1])
    idx = QUARTER_ORDER.index(season) if season in QUARTER_ORDER else 0
    next_idx = (idx + 1) % len(QUARTER_ORDER)
    next_year = year + 1 if next_idx == 0 else year
    return f"{QUARTER_ORDER[next_idx]} {next_year}"


def generate_plan(request: PlanRequest) -> GeneratePlanResponse:
    completed_ids: set[str] = {
        c.course_id.strip().upper()
        for c in request.transcript.courses
    }

    # Collect all missing courses from unfulfilled requirements
    todo: list[tuple[str, str, float]] = []  # (course_id, reason, units)
    for req in request.dar.requirements:
        if req.status == "complete" or req.units_applied >= req.units_required:
            continue
        remaining_units = req.units_required - req.units_applied
        added = 0.0
        for course_id in req.courses:
            if course_id.upper() not in completed_ids and added < remaining_units:
                todo.append((course_id, req.requirement, 4.0))
                added += 4.0

    # Determine starting term
    terms = [c.term for c in request.transcript.courses if c.term]
    last_term = max(terms) if terms else "Fall 2024"
    current_term = _next_term(last_term)

    quarters: list[QuarterPlan] = []
    max_units = request.max_units_per_quarter

    while todo:
        bucket: list[PlannedCourse] = []
        units_this_quarter = 0.0
        remaining_todo: list[tuple[str, str, float]] = []

        for course_id, reason, units in todo:
            if units_this_quarter + units <= max_units:
                bucket.append(
                    PlannedCourse(
                        course_id=course_id,
                        title=course_id,
                        units=units,
                        reason=f"Required for: {reason}",
                    )
                )
                units_this_quarter += units
            else:
                remaining_todo.append((course_id, reason, units))

        if bucket:
            quarters.append(
                QuarterPlan(
                    term=current_term,
                    courses=bucket,
                    total_units=units_this_quarter,
                )
            )
            current_term = _next_term(current_term)

        if remaining_todo == todo:
            # Nothing fit — safety exit
            break
        todo = remaining_todo

    estimated = quarters[-1].term if quarters else None
    notes: list[str] = []
    if not request.dar.requirements:
        notes.append("No DAR requirements loaded — upload a DAR to generate a detailed plan.")
    if not quarters:
        notes.append("All requirements appear complete based on provided transcript and DAR.")

    return GeneratePlanResponse(
        quarters=quarters,
        estimated_graduation=estimated,
        notes=notes,
    )
