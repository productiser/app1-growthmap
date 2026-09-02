from decimal import Decimal

from psycopg2 import connect

from app.qualifications.llm_inference_client import OPENROUTER_BASE_URL
from app.qualifications.service import run_qualification_inference


conn = None


def json_safe(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


try:
    conn = connect(dbname="growthmap")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            qr.id,
            qr.prospect_id,
            p.normalized_domain,
            p.first_submitted_url,
            p.country_code,
            p.language_code
        FROM qualification_requests qr
        JOIN prospects p ON p.id = qr.prospect_id
        ORDER BY qr.id DESC
        LIMIT 1
        """
    )
    qualification = cur.fetchone()
    if qualification is None:
        raise ValueError("No qualification_requests row found")

    (
        qualification_id,
        prospect_id,
        normalised_domain,
        normalised_url,
        country_code,
        language_code,
    ) = qualification

    cur.execute(
        """
        SELECT
            keyword,
            ranking_url,
            ranking_position,
            search_volume,
            cpc,
            competition
        FROM ranked_keywords
        WHERE prospect_id = %s
        ORDER BY id DESC
        LIMIT 20
        """,
        (prospect_id,),
    )
    ranked_keywords = [
        {
            "keyword": row[0],
            "ranking_url": row[1],
            "ranking_position": row[2],
            "search_volume": json_safe(row[3]),
            "cpc": json_safe(row[4]),
            "competition": json_safe(row[5]),
        }
        for row in cur.fetchall()
    ]

    cur.execute(
        """
        SELECT
            final_url,
            http_status,
            https_enabled,
            title,
            meta_description,
            h1,
            canonical_url,
            redirected,
            fetch_duration_ms,
            description_to_content_consistency
        FROM page_checks
        WHERE prospect_id = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (prospect_id,),
    )
    page_check_row = cur.fetchone()
    page_check = None
    if page_check_row is not None:
        page_check = {
            "final_url": page_check_row[0],
            "http_status": page_check_row[1],
            "https_enabled": page_check_row[2],
            "title": page_check_row[3],
            "meta_description": page_check_row[4],
            "h1": page_check_row[5],
            "canonical_url": page_check_row[6],
            "redirected": page_check_row[7],
            "fetch_duration_ms": json_safe(page_check_row[8]),
            "description_to_content_consistency": json_safe(page_check_row[9]),
        }

    llm_input = {
        "qualification_id": qualification_id,
        "prospect_id": prospect_id,
        "normalised_domain": normalised_domain,
        "normalised_url": normalised_url,
        "country_code": country_code,
        "language_code": language_code,
        "ranked_keywords": ranked_keywords,
        "page_check": page_check,
    }

    print("LLM input ranked keyword count:", len(ranked_keywords))
    print("LLM input has page_check:", page_check is not None)

    result = run_qualification_inference(
        conn,
        qualification_id=qualification_id,
        prospect_id=prospect_id,
        llm_input=llm_input,
    )
    print("LLM inference result:", result)

    cur.execute(
        """
        SELECT
            id,
            status,
            provider,
            stage,
            endpoint,
            request_json,
            response_json,
            cost_amount,
            error_message
        FROM provider_calls
        WHERE qualification_request_id = %s
          AND prospect_id = %s
          AND stage = 'qualification_inference'
        ORDER BY id DESC
        LIMIT 1
        """,
        (qualification_id, prospect_id),
    )
    provider_call = cur.fetchone()
    print("Stored provider call:", provider_call)

    assert provider_call is not None
    assert provider_call[1] == "completed"
    assert provider_call[2] == "openrouter-openai-gpt-latest"
    assert provider_call[3] == "qualification_inference"
    assert provider_call[4] == OPENROUTER_BASE_URL
    assert provider_call[5]["qualification_id"] == qualification_id
    assert provider_call[6] is not None

    conn.commit()
    print("Committed provider_call_id:", provider_call[0])

finally:
    if conn is not None:
        conn.close()
