import re
import io
from app.models.schemas import ParseDARResponse, DARRequirement

try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


def _extract_text(pdf_bytes: bytes) -> str:
    if PYMUPDF_AVAILABLE:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    if PDFPLUMBER_AVAILABLE:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    raise RuntimeError("No PDF parsing library available")


def _infer_status(line: str) -> str:
    upper = line.upper()
    if "COMPLETE" in upper or "SATISFIED" in upper or "OK" in upper:
        return "complete"
    if "IN PROGRESS" in upper or "IP" in upper:
        return "in_progress"
    return "incomplete"


def parse_dar(pdf_bytes: bytes) -> ParseDARResponse:
    text = _extract_text(pdf_bytes)
    requirements: list[DARRequirement] = []
    major: str | None = None
    total_required = 0.0
    total_applied = 0.0

    major_match = re.search(r"Major[:\s]+(.+)", text)
    if major_match:
        major = major_match.group(1).strip()

    # DAR section headers + requirement rows (heuristic)
    section_pattern = re.compile(
        r"(REQUIREMENT|AREA|GROUP)[:\s]+(.+?)\s+([\d.]+)\s+UNITS?\s+REQUIRED\s+([\d.]+)\s+UNITS?\s+APPLIED",
        re.IGNORECASE | re.MULTILINE,
    )
    for m in section_pattern.finditer(text):
        category, req_name, req_units, applied_units = m.groups()
        req = float(req_units)
        applied = float(applied_units)
        total_required += req
        total_applied += applied
        requirements.append(
            DARRequirement(
                category=category.title(),
                requirement=req_name.strip(),
                status=_infer_status(m.group(0)),
                units_required=req,
                units_applied=applied,
            )
        )

    return ParseDARResponse(
        major=major,
        requirements=requirements,
        total_required=total_required,
        total_applied=total_applied,
    )
