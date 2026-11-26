from app.db.db_connection import get_connection
from dotenv import load_dotenv
load_dotenv()
def main():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT product_id, product_cost FROM products ORDER BY product_id ASC;""")
            rows =cursor.fetchall()
            return rows
    finally:
        conn.close()
if __name__=="__main__":
    rows =main()
    print("DB_CONNECTED:", "TRUE" if rows is not None else "FAIL")
    print(f"PRODUCTS:",rows )