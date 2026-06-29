from fastapi import APIRouter, HTTPException

from app.qualifications.schemas import QualificationStartRequest, QualificationStartResponse
from app.qualifications.service import start_qualification

router = APIRouter(prefix="/qualify", tags=["qualifications"])


@router.post("/start", response_model=QualificationStartResponse)
def start_free_qualification(request: QualificationStartRequest):
    try:
        return start_qualification(
            business_url=request.business_url,
            email=request.email,
            country_code=request.country_code,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
