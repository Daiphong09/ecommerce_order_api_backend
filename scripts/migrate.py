from dotenv import load_dotenv
from pathlib import Path
from app.db.db_connection import get_connection

load_dotenv()
def migration():
    sql_file = (Path(__file__).resolve().parent.parent
                        /"database"/"migration"/"001_create_tables.sql")
    sql = sql_file.read_text(encoding="utf-8")
    conn =get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (
                                            version VARCHAR(100) PRIMARY KEY,
                                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                                                                        )""")
            cursor.execute("""SELECT 1 FROM schema_migrations 
                            WHERE version=%s""",("001_create_tables",))
            already_applied = cursor.fetchone()
            if already_applied:
                print("MIGRATION: SKIP")
            else:
                cursor.execute(sql)
                cursor.execute("""INSERT INTO schema_migrations
                    (version) VALUES (%s)""",("001_create_tables",))
                print("MIGRATION 001: APPLIED")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
if __name__=="__main__":
    migration()
