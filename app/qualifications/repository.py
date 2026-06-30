import psycopg2
from psycopg2 import connect
from dotenv import load_dotenv
import os
import logging

load_dotenv()
db_connection = os.getenv("DATABASE_URL")
logger = logging.getLogger(__name__)

# This function creates or updates a user record and returns a user id.
def get_or_create_user(email):
  with connect(db_connection) as conn:
    with conn.cursor() as cursor:
      cursor.execute("INSERT INTO users(email) VALUES (%s) ON CONFLICT (email) DO UPDATE SET UPDATED_AT=current_timestamp RETURNING id",(email,))
      user_id = cursor.fetchone()[0]
      logger.info(f"User id returned is:{user_id}")
      return user_id

def get_or_create_prospect(normalized_domain, submitted_url,country_code,language_code):
  with connect(db_connection) as conn:
    with conn.cursor() as cursor: 
      cursor.execute("INSERT INTO prospects(normalized_domain,first_submitted_url,country_code,language_code) values (%s,%s,%s,%s) ON CONFLICT (normalized_domain) DO UPDATE SET last_seen_at=current_timestamp RETURNING id",(normalized_domain,submitted_url,country_code,language_code))
      prospect_id = cursor.fetchone()[0]
      logger.info(f"Prospect id returned is:{prospect_id}")
      return prospect_id

def create_qualification_request(user_id,prospect_id, public_access_token,submitted_url):
  with connect(db_connection) as conn: 
      with conn.cursor() as cursor:
        cursor.execute("INSERT INTO qualification_requests(user_id,prospect_id,public_access_token,submitted_url) VALUES (%s,%s,%s,%s) RETURNING id",(user_id,prospect_id,public_access_token,submitted_url))
        qualification_id= cursor.fetchone()[0]
        logger.info(f"Qualification id created is:{qualification_id}")
        return qualification_id
