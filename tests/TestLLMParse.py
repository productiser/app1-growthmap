from app.qualifications.service import parse_llm_content
from psycopg2 import connect

conn = None


def test_openrouter_usage_fields_are_extracted():
  try:
      conn = connect(dbname="growthmap")
      cur = conn.cursor()
      cur.execute(
              """
              SELECT response_json
              FROM provider_calls
              WHERE provider = 'openrouter-openai-gpt-latest'
                AND status = 'completed'
              ORDER BY id DESC
              LIMIT 1
              """
          )
      response_json = cur.fetchone()[0]
      row = parse_llm_content(response_json)
      if row is None:
          raise ValueError("No page_check row could be extracted")
      print(row)

      #get content as a JSON
      print(row)
      print(type(row))
      


    
  finally:
      conn.close()

if __name__ == "__main__":
    test_openrouter_usage_fields_are_extracted()
    print("LLM inference client usage extraction ok")
