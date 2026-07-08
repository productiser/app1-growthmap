import logging
from typing import Any

from psycopg2.extras import Json

logger = logging.getLogger(__name__)

# This function creates or updates a user record and returns a user id.
def get_or_create_user(conn, email: str) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users(email)
            VALUES (%s)
            ON CONFLICT (email)
            DO UPDATE SET updated_at = CURRENT_TIMESTAMP
            RETURNING id
            """,
            (email,),
        )
        user_id = cursor.fetchone()[0]
        logger.info(f"User id returned is:{user_id}")
        return user_id

def get_or_create_prospect(
    conn,
    normalized_domain: str,
    submitted_url: str,
    country_code: str,
    language_code: str,
) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO prospects (
                normalized_domain,
                first_submitted_url,
                country_code,
                language_code
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (normalized_domain)
            DO UPDATE SET last_seen_at = CURRENT_TIMESTAMP
            RETURNING id
            """,
            (normalized_domain, submitted_url, country_code, language_code),
        )
        prospect_id = cursor.fetchone()[0]
        logger.info(f"Prospect id returned is:{prospect_id}")
        return prospect_id

def create_qualification_request(
    conn,
    user_id: int,
    prospect_id: int,
    public_access_token: str,
    submitted_url: str,
) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO qualification_requests (
                user_id,
                prospect_id,
                public_access_token,
                submitted_url
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (user_id, prospect_id, public_access_token, submitted_url),
        )
        qualification_id = cursor.fetchone()[0]
        logger.info(f"Qualification id created is:{qualification_id}")
        return qualification_id

def create_provider_call(
    conn,
    qualification_request_id: int,
    prospect_id: int,
    provider: str,
    stage: str,
    endpoint: str,
    request_json: list[dict[str, Any]],
) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO provider_calls (
                qualification_request_id,
                prospect_id,
                provider,
                stage,
                endpoint,
                status,
                request_json,
                started_at
            )
            VALUES (%s, %s, %s, %s, %s, 'running', %s, CURRENT_TIMESTAMP)
            RETURNING id
            """,
            (
                qualification_request_id,
                prospect_id,
                provider,
                stage,
                endpoint,
                Json(request_json),
            ),
        )
        provider_call_id = cursor.fetchone()[0]
        logger.info(f"Provider call id created is:{provider_call_id}")
        return provider_call_id

def mark_provider_call_completed(
    conn,
    provider_call_id: int,
    response_json: dict[str, Any],
    provider_task_id: str | None,
    cost_amount: float | None,
) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE provider_calls
            SET status = 'completed',
                provider_task_id = %s,
                response_json = %s,
                cost_amount = %s,
                cost_currency = 'USD',
                completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (provider_task_id, Json(response_json), cost_amount, provider_call_id),
        )

def mark_provider_call_failed(
    conn,
    provider_call_id: int,
    error_message: str,
) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE provider_calls
            SET status = 'failed',
                error_message = %s,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (error_message, provider_call_id),
        )

def create_ranked_keywords(
    conn,
    prospect_id: int,
    provider_call_id: int,
    ranked_keywords: list[dict[str, Any]],
) -> None:
    with conn.cursor() as cursor:
        for keyword_row in ranked_keywords:
            cursor.execute(
                """
                INSERT INTO ranked_keywords (
                    prospect_id,
                    provider_call_id,
                    keyword,
                    ranking_url,
                    ranking_position,
                    search_volume,
                    cpc,
                    competition
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    prospect_id,
                    provider_call_id,
                    keyword_row.get("keyword"),
                    keyword_row.get("ranking_url"),
                    keyword_row.get("ranking_position"),
                    keyword_row.get("search_volume"),
                    keyword_row.get("cpc"),
                    keyword_row.get("competition"),
                ),
            )
            logger.info("Extracted keyword inserted")
