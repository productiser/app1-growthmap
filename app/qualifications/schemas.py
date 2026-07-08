from pydantic import BaseModel


class MarketContext(BaseModel):
    country_code: str
    language_code: str

class DataForSeoEvidenceStatus(BaseModel):
    status: str
    ranked_keywords_call_id: int | None
    on_page_call_id: int | None
    error: str | None


class QualificationStartRequest(BaseModel):
    business_url: str
    email: str
    country_code: str


class QualificationStartResponse(BaseModel):
    status: str
    submitted_url: str
    normalised_url: str
    normalised_domain: str
    user_id:int
    prospect_id:int
    qualification_id:int
    email: str
    market: MarketContext
    public_access_token: str
    dataforseo: DataForSeoEvidenceStatus
    next_step: str
    limitations: list[str]
