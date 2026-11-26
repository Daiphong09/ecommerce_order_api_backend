from pathlib import Path
from dotenv import load_dotenv
from app.db.db_connection import get_connection

load_dotenv()

def run_seed():
    sql_seed = (Path(__file__).resolve().parent.parent/"database"/"seeds"/"001_seed_products.sql")
    sql = sql_seed.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        print("SEEDED PRODUCTS")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
if __name__=="__main__":
    run_seed()