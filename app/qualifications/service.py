import logging
import secrets
from urllib.parse import urlparse


logger = logging.getLogger(__name__)

SUPPORTED_COUNTRY_CODES = {"GB", "US", "CA", "AU", "IN"}
DEFAULT_LANGUAGE_CODE = "en"


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
    if country_code not in SUPPORTED_COUNTRY_CODES:
        supported = ", ".join(sorted(SUPPORTED_COUNTRY_CODES))
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

    return {
        "status": "validated",
        "submitted_url": business_url,
        "normalised_url": normalised_url,
        "normalised_domain": normalised_domain,
        "email": normalised_email,
        "market": {
            "country_code": normalised_country_code,
            "language_code": DEFAULT_LANGUAGE_CODE,
        },
        "public_access_token": public_access_token,
        "next_step": "create_user_prospect_and_qualification_request",
        "limitations": [
            "No DataForSEO, LLM, scoring or result generation has run yet.",
            "Database creation is the next implementation slice.",
        ],
    }
