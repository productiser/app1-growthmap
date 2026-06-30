import logging
import secrets
from urllib.parse import urlparse
from app.qualifications.repository import get_or_create_user,get_or_create_prospect,create_qualification_request


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

    # 1. Create or reuse user based on email id. 
    user_id = get_or_create_user(normalised_email)

    # 2. Create a reusable prospect
    prospect_id = get_or_create_prospect(normalised_domain,normalised_url,normalised_country_code, market["language_code"])

    #3. Create qualification request. 
    qualification_id=create_qualification_request(user_id=user_id,prospect_id=prospect_id,public_access_token=public_access_token,submitted_url=normalised_url)

    return {
        "status": "validated",
        "submitted_url": business_url,
        "normalised_url": normalised_url,
        "normalised_domain": normalised_domain,
        "email": normalised_email,
        "user_id":user_id,
        "prospect_id": prospect_id,
        "qualification_id":qualification_id,
        "market": {
            "country_code": normalised_country_code,
            "language_code": market["language_code"],
        },
        "public_access_token": public_access_token,
        "next_step": "create_user_prospect_and_qualification_request",
        "limitations": [
            "No DataForSEO, LLM, scoring or result generation has run yet.",
        ],
    }
