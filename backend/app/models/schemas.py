from pydantic import BaseModel
from typing import Optional


class Major(BaseModel):
    id: str
    name: str
    department: str
    total_units: int
    description: Optional[str] = None


class TranscriptCourse(BaseModel):
    course_id: str
    title: str
    units: float
    grade: str
    term: str


class ParseTranscriptResponse(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    total_units: float = 0.0
    courses: list[TranscriptCourse] = []


class DARRequirement(BaseModel):
    category: str
    requirement: str
    status: str  # "complete", "in_progress", "incomplete"
    units_required: float
    units_applied: float
    courses: list[str] = []


class ParseDARResponse(BaseModel):
    major: Optional[str] = None
    requirements: list[DARRequirement] = []
    total_required: float = 0.0
    total_applied: float = 0.0


class AuditRequest(BaseModel):
    transcript: ParseTranscriptResponse
    dar: ParseDARResponse


class AuditResult(BaseModel):
    requirement: str
    status: str
    missing_courses: list[str] = []
    notes: Optional[str] = None


class AuditResponse(BaseModel):
    major: Optional[str] = None
    passed: list[AuditResult] = []
    pending: list[AuditResult] = []
    failed: list[AuditResult] = []
    completion_percentage: float = 0.0


class PlanRequest(BaseModel):
    transcript: ParseTranscriptResponse
    dar: ParseDARResponse
    target_graduation_term: Optional[str] = None
    max_units_per_quarter: int = 20


class PlannedCourse(BaseModel):
    course_id: str
    title: str
    units: float
    reason: str


class QuarterPlan(BaseModel):
    term: str
    courses: list[PlannedCourse] = []
    total_units: float = 0.0


class GeneratePlanResponse(BaseModel):
    quarters: list[QuarterPlan] = []
    estimated_graduation: Optional[str] = None
    notes: list[str] = []
