import logging
import os
import secrets
from typing import Any
from urllib.parse import urlparse
import json
from dotenv import load_dotenv
from psycopg2 import connect


from app.qualifications.dataforseo_client import (
    DataForSeoApiError,
    DataForSeoClient,
    DataForSeoConfigurationError,
    build_on_page_payload,
    build_ranked_keywords_payload,
)
from app.qualifications.llm_inference_client import (
    LLMInferenceClient,
    LLMInferenceConfigError,
    OPENROUTER_BASE_URL,
)
from app.qualifications.repository import (
    create_onpage_checks,
    create_provider_call,
    create_qualification_request,
    create_ranked_keywords,
    get_or_create_prospect,
    get_or_create_user,
    mark_provider_call_completed,
    mark_provider_call_failed,
)

load_dotenv()
db_connection = os.getenv("DATABASE_URL")

logger = logging.getLogger(__name__)

SUPPORTED_MARKETS = {
    "GB": {
        "label": "United Kingdom",
        "language_code": "en",
        "dataforseo_location_code": 2826,
    },
    "US": {
        "label": "United States",
        "language_code": "en",
        "dataforseo_location_code": 2840,
    },
    "CA": {
        "label": "Canada",
        "language_code": "en",
        "dataforseo_location_code": 2124,
    },
    "AU": {
        "label": "Australia",
        "language_code": "en",
        "dataforseo_location_code": 2036,
    },
    "IN": {
        "label": "India",
        "language_code": "en",
        "dataforseo_location_code": 2356,
    },
}


def normalise_submitted_url(raw_url: str) -> str:
    cleaned_url = raw_url.strip()
    if not cleaned_url:
        raise ValueError("Business URL is required")

    if not cleaned_url.startswith(("http://", "https://")):
        cleaned_url = f"https://{cleaned_url}"

    parsed_url = urlparse(cleaned_url)
    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Business URL must use http or https")
    if not parsed_url.netloc:
        raise ValueError("Business URL must include a domain")

    return cleaned_url


def extract_normalised_domain(normalised_url: str) -> str:
    parsed_url = urlparse(normalised_url)
    domain = parsed_url.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]
    if not domain:
        raise ValueError("Could not extract domain from business URL")

    return domain


def normalise_email(raw_email: str) -> str:
    email = raw_email.strip().lower()
    if not email:
        raise ValueError("Email is required")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Email must look like a valid email address")

    return email


def normalise_country_code(raw_country_code: str) -> str:
    country_code = raw_country_code.strip().upper()
    if country_code not in SUPPORTED_MARKETS:
        supported = ", ".join(sorted(SUPPORTED_MARKETS))
        raise ValueError(f"Country code must be one of: {supported}")

    return country_code


def generate_public_access_token() -> str:
    return secrets.token_urlsafe(32)


def run_dataforseo_evidence_calls(
    conn,
    qualification_id: int,
    prospect_id: int,
    normalised_domain: str,
    normalised_url: str,
    market: dict,
) -> dict:
    evidence_summary = {
        "status": "skipped",
        "ranked_keywords_call_id": None,
        "on_page_call_id": None,
        "error": None,
    }

    try:
        dataforseo_client = DataForSeoClient()
    except DataForSeoConfigurationError as error:
        evidence_summary["error"] = str(error)
        return {
            "summary": evidence_summary,
            "parsed_evidence": {
                "ranked_keywords": [],
                "page_check": None,
            },
        }

    ranked_keywords_response = None
    ranked_keywords_call_id = None
    on_page_response = None
    on_page_call_id = None
    ranked_keywords = []
    onpage_extract = None

    try:
        ranked_keywords_request = build_ranked_keywords_payload(
            target_domain=normalised_domain,
            location_code=market["dataforseo_location_code"],
            language_code=market["language_code"],
            limit=20,
        )
        ranked_keywords_call_id = create_provider_call(
            conn,
            qualification_request_id=qualification_id,
            prospect_id=prospect_id,
            provider="dataforseo",
            stage="ranked_keywords",
            endpoint="/dataforseo_labs/google/ranked_keywords/live",
            request_json=ranked_keywords_request,
        )
        evidence_summary["ranked_keywords_call_id"] = ranked_keywords_call_id
        ranked_keywords_response = dataforseo_client.fetch_ranked_keywords(
            target_domain=normalised_domain,
            location_code=market["dataforseo_location_code"],
            language_code=market["language_code"],
            limit=20,
        )

        mark_provider_call_completed(
            conn,
            provider_call_id=ranked_keywords_call_id,
            response_json=ranked_keywords_response.response_json,
            provider_task_id=ranked_keywords_response.provider_task_id,
            cost_amount=ranked_keywords_response.cost,
        )

        ranked_keywords = extract_ranked_keywords_rows(ranked_keywords_response.response_json)
        create_ranked_keywords(
            conn,
            prospect_id=prospect_id,
            provider_call_id=ranked_keywords_call_id,
            ranked_keywords=ranked_keywords,
        )

        on_page_request = build_on_page_payload(normalised_url)
        on_page_call_id = create_provider_call(
            conn,
            qualification_request_id=qualification_id,
            prospect_id=prospect_id,
            provider="dataforseo",
            stage="on_page",
            endpoint="/on_page/instant_pages",
            request_json=on_page_request,
        )
        evidence_summary["on_page_call_id"] = on_page_call_id
        on_page_response = dataforseo_client.fetch_on_page(normalised_url)

        mark_provider_call_completed(
            conn,
            provider_call_id=on_page_call_id,
            response_json=on_page_response.response_json,
            provider_task_id=on_page_response.provider_task_id,
            cost_amount=on_page_response.cost,
        )
        onpage_extract = extract_page_check_row(on_page_response.response_json)
        if onpage_extract is not None:
            create_onpage_checks(
                conn,
                prospect_id=prospect_id,
                provider_call_id=on_page_call_id,
                checked_url=normalised_url,
                onpage_extract=onpage_extract,
            )
        else:
            logger.warning(
                "No page_check row extracted for provider_call_id=%s",
                on_page_call_id,
            )
    except DataForSeoApiError as error:
        if on_page_call_id and on_page_response is None:
            mark_provider_call_failed(conn, on_page_call_id, str(error))
        elif ranked_keywords_call_id and ranked_keywords_response is None:
            mark_provider_call_failed(conn, ranked_keywords_call_id, str(error))
        evidence_summary["status"] = "failed"
        evidence_summary["error"] = str(error)
        return {
            "summary": evidence_summary,
            "parsed_evidence": {
                "ranked_keywords": ranked_keywords,
                "page_check": onpage_extract,
            },
        }

    evidence_summary["status"] = "completed"

    return {
        "summary": evidence_summary,
        "parsed_evidence": {
            "ranked_keywords": ranked_keywords,
            "page_check": onpage_extract,
        },
    }


# Extract ranked keywords and parse before storing.
def extract_ranked_keywords_rows(response_json: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = response_json.get("tasks") or []
    if not tasks:
        return []

    results = tasks[0].get("result") or []
    if not results:
        return []

    items = results[0].get("items") or []
    if not items:
        return []

    rows = []

    for item in items:
        keyword_data = item.get("keyword_data") or {}
        keyword_info = keyword_data.get("keyword_info") or {}
        serp_item = (item.get("ranked_serp_element") or {}).get("serp_item") or {}
        keyword = keyword_data.get("keyword")
        if not keyword:
            continue

        rows.append(
            {
                "keyword": keyword,
                "ranking_url": serp_item.get("url"),
                "ranking_position": serp_item.get("rank_absolute"),
                "search_volume": keyword_info.get("search_volume"),
                "cpc": keyword_info.get("cpc"),
                "competition": keyword_info.get("competition"),
            }
        )

    return rows

def extract_page_check_row(response_json: dict[str, Any]) -> dict[str, Any] | None:
    tasks = response_json.get("tasks") or []
    if not tasks:
        return None

    results = tasks[0].get("result") or []
    if not results:
        return None

    items = results[0].get("items") or []
    if not items:
        return None

    item = items[0] or {}
    checks = item.get("checks") or {}
    meta = item.get("meta") or {}
    page_timing = item.get("page_timing") or {}
    htags = meta.get("htags") or {}
    content = meta.get("content") or {}

    h1_values = htags.get("h1") or []
    h1 = h1_values[0] if h1_values else None

    return {
        "final_url": item.get("url"),
        "onpage_score": item.get("onpage_score"),
        "http_status": item.get("status_code"),
        "https_enabled": checks.get("is_https"),
        "redirected": checks.get("is_redirect"),
        "title": meta.get("title"),
        "meta_description": meta.get("description"),
        "h1": h1,
        "canonical_url": meta.get("canonical"),
        "fetch_duration_ms": page_timing.get("duration_time"),
        "description_to_content_consistency": content.get(
            "description_to_content_consistency"
        ),
    }

def parse_llm_content(response_json:dict[str,Any])->dict[str,Any]:
    content_str =  response_json["choices"][0]["message"]["content"]
    print(content_str[4680:4820])
    print(repr(content_str[4680:4820]))
    return json.loads(content_str)

# LLM Inference call for qualification
def run_qualification_inference(conn, qualification_id:int, prospect_id:int, llm_input: dict) -> dict:
    try:

        provider_call_id = create_provider_call(conn,
        qualification_id,
        prospect_id,
        provider= "openrouter-openai-gpt-latest",
        stage= "qualification_inference",
        endpoint= OPENROUTER_BASE_URL,
        request_json=llm_input)

        llm_client = LLMInferenceClient()

        llm_response = llm_client.run_qualification_inference(llm_input)

        mark_provider_call_completed( conn,
        provider_call_id=provider_call_id,
        response_json=llm_response.response_json,
        provider_task_id =None ,
        cost_amount= llm_response.cost,
        input_tokens=llm_response.input_tokens,
        output_tokens=llm_response.output_tokens)

        #Extract data from LLM response.
        llm_content_text = parse_llm_content(llm_response.response_json)


    except LLMInferenceConfigError as error:
        mark_provider_call_failed(conn, provider_call_id, str(error))
        return {
            "status":"failed",
            "provider_call_id":provider_call_id,
            "error":str(error)
        }
    return llm_response


def start_qualification(business_url: str, email: str, country_code: str) -> dict:
    normalised_url = normalise_submitted_url(business_url)
    normalised_domain = extract_normalised_domain(normalised_url)
    normalised_email = normalise_email(email)
    normalised_country_code = normalise_country_code(country_code)
    public_access_token = generate_public_access_token()

    logger.info(
        "Qualification start validated for domain=%s country=%s",
        normalised_domain,
        normalised_country_code,
    )
    market = SUPPORTED_MARKETS[normalised_country_code]

    with connect(db_connection) as conn:

        # 1. Create or reuse user based on email id.
        user_id = get_or_create_user(conn, normalised_email)

        # 2. Create a reusable prospect
        prospect_id = get_or_create_prospect(
            conn,
            normalised_domain,
            normalised_url,
            normalised_country_code,
            market["language_code"],
        )

        # 3. Create qualification request.
        qualification_id = create_qualification_request(
            conn,
            user_id=user_id,
            prospect_id=prospect_id,
            public_access_token=public_access_token,
            submitted_url=normalised_url,
        )

        # 4. Collect first external SEO evidence after the email-gated request exists.
        dataforseo = run_dataforseo_evidence_calls(
            conn,
            qualification_id=qualification_id,
            prospect_id=prospect_id,
            normalised_domain=normalised_domain,
            normalised_url=normalised_url,
            market=market,
        )

        # 5.1 Create inference input payload.
        llm_input = {
            "qualification_id": qualification_id,
            "prospect_id": prospect_id,
            "normalised_domain": normalised_domain,
            "normalised_url": normalised_url,
            "country_code": normalised_country_code,
            "language_code": market["language_code"],
            "ranked_keywords": dataforseo["parsed_evidence"]["ranked_keywords"],
            "page_check": dataforseo["parsed_evidence"]["page_check"],
        }

        #5. Run the LLM Inference call on qualification.
        llm_inference = run_qualification_inference(conn,qualification_id,prospect_id, llm_input)

    return {
        "status": "validated",
        "submitted_url": business_url,
        "normalised_url": normalised_url,
        "normalised_domain": normalised_domain,
        "email": normalised_email,
        "user_id": user_id,
        "prospect_id": prospect_id,
        "qualification_id": qualification_id,
         "dataforseo": dataforseo["summary"],
        "market": {
            "country_code": normalised_country_code,
            "language_code": market["language_code"],
        },
        "public_access_token": public_access_token,
       
        "next_step": "classify_ranked_keyword_evidence",
        "limitations": [
            "No LLM, scoring or result generation has run yet."
        ],
    }
