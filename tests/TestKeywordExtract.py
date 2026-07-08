from app.qualifications.repository import create_ranked_keywords
from app.qualifications.service import extract_ranked_keywords_rows
from psycopg2 import connect


try:
    conn = connect(dbname="growthmap")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, prospect_id, response_json
        FROM provider_calls
        WHERE stage = 'ranked_keywords'
          AND status = 'completed'
        ORDER BY id DESC
        LIMIT 1
        """
    )
    provider_call_id, prospect_id, response_json = cur.fetchone()
    rows = extract_ranked_keywords_rows(response_json)
    print(rows[0])

    create_ranked_keywords(
        conn,
        prospect_id=prospect_id,
        provider_call_id=provider_call_id,
        ranked_keywords=rows,
    )
    cur.execute(
        "SELECT count(*) FROM ranked_keywords WHERE provider_call_id = %s",
        (provider_call_id,),
    )
    print("Rows inside transaction:", cur.fetchone()[0])
    conn.rollback()
    print("Rolled back")
finally:
    conn.close()
