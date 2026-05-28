from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.schemas import ParseDARResponse, ParseTranscriptResponse
from app.services.dar_parser import parse_dar
from app.services.transcript_parser import parse_transcript

router = APIRouter()

_MAX_BYTES = 20 * 1024 * 1024  # 20 MB


def _validate_pdf(file: UploadFile) -> None:
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="File must be a PDF")


@router.post("/parse-transcript", response_model=ParseTranscriptResponse)
async def parse_transcript_route(file: UploadFile = File(...)):
    _validate_pdf(file)
    data = await file.read(_MAX_BYTES)
    try:
        return parse_transcript(data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/parse-dar", response_model=ParseDARResponse)
async def parse_dar_route(file: UploadFile = File(...)):
    _validate_pdf(file)
    data = await file.read(_MAX_BYTES)
    try:
        return parse_dar(data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
