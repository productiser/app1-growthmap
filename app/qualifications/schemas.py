from pydantic import BaseModel


class MarketContext(BaseModel):
    country_code: str
    language_code: str


class QualificationStartRequest(BaseModel):
    business_url: str
    email: str
    country_code: str


class QualificationStartResponse(BaseModel):
    status: str
    submitted_url: str
    normalised_url: str
    normalised_domain: str
    email: str
    market: MarketContext
    public_access_token: str
    next_step: str
    limitations: list[str]
