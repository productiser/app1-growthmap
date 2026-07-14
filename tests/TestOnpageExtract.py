from app.qualifications.repository import create_onpage_checks
from app.qualifications.service import extract_page_check_row
from psycopg2 import connect


try:
    conn = connect(dbname="growthmap")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, prospect_id, response_json
        FROM provider_calls
        WHERE stage = 'on_page'
          AND status = 'completed'
        ORDER BY id DESC
        LIMIT 1
        """
    )
    provider_call_id, prospect_id, response_json = cur.fetchone()
    row = extract_page_check_row(response_json)
    if row is None:
        raise ValueError("No page_check row could be extracted")
    print(row)

    create_onpage_checks(
        conn,
        prospect_id=prospect_id,
        provider_call_id=provider_call_id,
        checked_url=row["final_url"],
        onpage_extract=row,
    )
    cur.execute(
        "SELECT count(*) FROM page_checks WHERE provider_call_id = %s",
        (provider_call_id,),
    )
    print("Rows inside transaction:", cur.fetchone()[0])
    conn.rollback()
    print("Rolled back")
    cur.execute(
        "SELECT count(*) FROM page_checks WHERE provider_call_id = %s",
        (provider_call_id,),
    )
    print("Rows after rollback:", cur.fetchone()[0])

finally:
    conn.close()
