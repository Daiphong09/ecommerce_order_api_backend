from app.core.config import get_env
import psycopg2 
def get_connection():
    setting = get_env()
    return psycopg2.connect(host=setting.get("DB_HOST"),
                            port=setting.get("DB_PORT"),
                            user=setting.get("DB_USER"),
                            dbname=setting.get("DB_NAME"),
                            password=setting.get("DB_PASSWORD"))
