"""GrowthMap V1: GrowthMap early FastAPI scaffold.

  This file is not yet aligned with the frozen qualification-first V1 flow.
  Current product/design source of truth:
  - Design/design.md
  - Design/module-design.md
"""

from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


load_dotenv()

app = FastAPI(title="GrowthMap")


# ===== PYDANTIC CONTRACTS =====


class GrowthMapRequest(BaseModel):
    """A freelancer's selected local-business prospect."""

    business_name: str
    business_url: HttpUrl
    city: str
    country: str
    service: str


class LocalBusinessResult(BaseModel):
    """One business observed in Maps or Local Finder."""

    business_name: str
    position: int | None = None
    category: str | None = None
    rating: float | None = None
    review_count: int | None = None
    website_url: str | None = None
    google_cid: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_target: bool = False


class VisibilityGap(str, Enum):
    TARGET_NOT_VISIBLE = "target_not_visible"
    TARGET_VISIBLE_BELOW_COMPETITORS = "target_visible_below_competitors"
    CATEGORY_OR_SERVICE_MISMATCH = "category_or_service_mismatch"
    REVIEW_TRUST_GAP = "review_trust_gap"
    NO_CLEAR_GAP = "no_clear_gap"


class LocalVisibilityEvidence(BaseModel):
    """Structured evidence calculated before the LLM call."""

    query: str
    location_code: int
    target_found: bool
    target_position: int | None = None
    visible_businesses: list[LocalBusinessResult]
    primary_gap: VisibilityGap


class GrowthMapResponse(BaseModel):
    """The final prospect brief returned to the GrowthMap user."""

    request_id: int
    business_name: str
    evidence: LocalVisibilityEvidence
    actions: list[str]
    pitch: str
    limitations: list[str]
    status: str


# ===== ROUTES =====


@app.get("/health")
def get_health():
    """TODO: Restore and adapt the Postgres health check after schema review."""

    return {"status": "ok"}


@app.post("/reports", response_model=GrowthMapResponse)
def create_report(report_request: GrowthMapRequest):
    """Orchestrate one Local Visibility Prospect Brief.

    Build order:
    1. Verify the user owns enough tokens.
    2. Insert report_requests and return its ID.
    3. Resolve the DataForSEO location code.
    4. Build one service-and-location query.
    5. Call the selected Maps or Local Finder endpoint.
    6. Parse and save local_search_runs/local_search_results.
    7. Match the target and calculate one VisibilityGap.
    8. Call the LLM for actions, pitch wording, and limitations.
    9. Save the final report.
    10. Charge one token only after successful completion.
    """

    location_code = get_location_code(
        city=report_request.city,
        country=report_request.country,
    )
    query = build_local_search_query(
        service=report_request.service,
        city=report_request.city,
    )
    visible_businesses = get_local_search_results(
        query=query,
        location_code=location_code,
    )
    evidence = analyse_local_visibility(
        target_business_name=report_request.business_name,
        query=query,
        location_code=location_code,
        visible_businesses=visible_businesses,
    )

    # TODO: Replace these values after database and LLM implementation.
    return GrowthMapResponse(
        request_id=0,
        business_name=report_request.business_name,
        evidence=evidence,
        actions=["TODO: generate three evidence-backed actions"],
        pitch="TODO: generate client-safe pitch wording",
        limitations=["This scaffold currently uses mocked local-search results."],
        status="scaffold",
    )


# ===== IMPLEMENTATION PLACEHOLDERS =====


def get_location_code(city: str, country: str) -> int:
    """TODO: Replace the fixed value with the agreed location lookup."""

    return 1006886


def build_local_search_query(service: str, city: str) -> str:
    """Build the one controlled query used by V1."""

    return f"{service} {city}".strip()


def get_local_search_results(
    query: str,
    location_code: int,
) -> list[LocalBusinessResult]:
    """TODO: Compare Maps and Local Finder, then implement one endpoint.

    First real slice:
    - make one authenticated request
    - inspect tasks[0].result
    - parse only fields represented by LocalBusinessResult
    - save the provider's actual cost
    """

    return get_mock_local_search_results()


def get_mock_local_search_results() -> list[LocalBusinessResult]:
    """Temporary fixture for exercising the route and response models."""

    return [
        LocalBusinessResult(
            business_name="Example Visible Business",
            position=1,
            category="Example category",
            rating=4.8,
            review_count=125,
            website_url="https://example.com",
            google_cid="example-cid",
            latitude=51.5074,
            longitude=-0.1278,
        )
    ]


def analyse_local_visibility(
    target_business_name: str,
    query: str,
    location_code: int,
    visible_businesses: list[LocalBusinessResult],
) -> LocalVisibilityEvidence:
    """TODO: Expand matching and gap rules using reviewed test cases."""

    normalized_target = normalize_business_name(target_business_name)
    target_result = next(
        (
            business
            for business in visible_businesses
            if normalize_business_name(business.business_name)
            == normalized_target
        ),
        None,
    )

    if target_result is None:
        primary_gap = VisibilityGap.TARGET_NOT_VISIBLE
    else:
        target_result.is_target = True
        primary_gap = VisibilityGap.NO_CLEAR_GAP

    return LocalVisibilityEvidence(
        query=query,
        location_code=location_code,
        target_found=target_result is not None,
        target_position=target_result.position if target_result else None,
        visible_businesses=visible_businesses,
        primary_gap=primary_gap,
    )


def normalize_business_name(name: str) -> str:
    """Start with minimal deterministic normalization."""

    return " ".join(name.lower().split())
