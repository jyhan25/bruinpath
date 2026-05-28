import re
from pathlib import Path
from app.models.schemas import ParseTranscriptResponse, TranscriptCourse

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


def _extract_text_pymupdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def _extract_text_pdfplumber(pdf_bytes: bytes) -> str:
    import io
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def _parse_grade(grade_str: str) -> str:
    grade_str = grade_str.strip()
    valid = {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "P", "NP", "W", "I", "IP"}
    return grade_str if grade_str in valid else "IP"


def parse_transcript(pdf_bytes: bytes) -> ParseTranscriptResponse:
    if PYMUPDF_AVAILABLE:
        text = _extract_text_pymupdf(pdf_bytes)
    elif PDFPLUMBER_AVAILABLE:
        text = _extract_text_pdfplumber(pdf_bytes)
    else:
        raise RuntimeError("No PDF parsing library available")

    courses: list[TranscriptCourse] = []
    gpa: float | None = None
    student_name: str | None = None
    major: str | None = None
    total_units = 0.0

    # UCLA transcript patterns (heuristic — will be refined with real samples)
    name_match = re.search(r"Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text)
    if name_match:
        student_name = name_match.group(1)

    major_match = re.search(r"Major[:\s]+(.+)", text)
    if major_match:
        major = major_match.group(1).strip()

    gpa_match = re.search(r"Cumulative GPA[:\s]+([\d.]+)", text)
    if gpa_match:
        gpa = float(gpa_match.group(1))

    # Course line: e.g. "CS  31     Introduction to CS     4.0   A"
    course_pattern = re.compile(
        r"([A-Z &]{2,10})\s+(\d{1,3}[A-Z]?)\s+(.+?)\s+([\d.]+)\s+([A-F][+\-]?|P|NP|W|I|IP)\s+(\w{4}\s+\d{4})?",
        re.MULTILINE,
    )
    for m in course_pattern.finditer(text):
        dept, num, title, units, grade, term = m.groups()
        course_id = f"{dept.strip()} {num.strip()}"
        u = float(units)
        total_units += u
        courses.append(
            TranscriptCourse(
                course_id=course_id,
                title=title.strip(),
                units=u,
                grade=_parse_grade(grade),
                term=(term or "").strip(),
            )
        )

    return ParseTranscriptResponse(
        student_name=student_name,
        major=major,
        gpa=gpa,
        total_units=total_units,
        courses=courses,
    )
