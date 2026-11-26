from app.orders.repository import insert_order,insert_order_items
from dotenv import load_dotenv
load_dotenv()
from app.db.db_connection import get_connection
def insert():
    conn = get_connection()
    order_id = "ORD-RB05-REPO-001"
    total_amount = 350000

    order_items = [
        {
            "product_id": "P101",
            "quantity": 2,
            "unit_price": 100000,
            "subtotal": 200000
        },
        {
            "product_id": "P102",
            "quantity": 3,
            "unit_price": 50000,
            "subtotal": 150000
        }
    ]
    try:
        with conn.cursor() as cursor:
            insert_order(cursor, order_id, total_amount)
            insert_order_items(cursor, order_id, order_items)
            cursor.execute("SELECT order_id FROM orders WHERE order_id=(%s);", (order_id,))
            row_orders =cursor.fetchall()
            cursor.execute("SELECT order_id FROM order_items WHERE order_id=(%s);",(order_id,))
            row_items = cursor.fetchall()
            assert len(row_orders) ==1
            assert len(row_items) ==2
            print("TEST_INSERT")
            print("ORDERS_IN_TX:", len(row_orders))
            print("ITEMS_IN_TX:", len(row_items))
    finally:
        conn.rollback()
        conn.close()
def rollback():
    conn = get_connection()
    order_id = "ORD-RB05-REPO-001"
    total_amount = 350000

    order_items = [
        {
            "product_id": "P101",
            "quantity": 2,
            "unit_price": 100000,
            "subtotal": 200000
        },
        {
            "product_id": "P102",
            "quantity": 3,
            "unit_price": 50000,
            "subtotal": 150000
        }
    ]
    try:
        with conn.cursor() as cursor:
            insert_order(cursor, order_id, total_amount)
            insert_order_items(cursor, order_id, order_items)
            cursor.execute("SELECT order_id FROM orders WHERE order_id=(%s);", (order_id,))
            row_orders_before =cursor.fetchall()
            cursor.execute("SELECT order_id FROM order_items WHERE order_id=(%s);",(order_id,))
            row_items_before = cursor.fetchall()
            assert len(row_orders_before) ==1
            assert len(row_items_before) ==2
            print("TEST_BEFORE_ROLLBACK")
            print("ORDERS_IN_TX:", len(row_orders_before))
            print("ITEMS_IN_TX:", len(row_items_before))
            conn.rollback()
    finally:
        conn.close()

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT order_id FROM orders WHERE order_id=(%s);", (order_id,))
            row_orders_after = cursor.fetchall()
            cursor.execute("SELECT order_id FROM order_items WHERE order_id=(%s);",(order_id,))
            row_items_after = cursor.fetchall()
            assert len(row_orders_after) ==0
            assert len(row_items_after) ==0
            print("ROLLBACK_SUCCESS")
            print("ORDERS_AFTER_ROLLBACK:", len(row_orders_after))
            print("ITEMS_AFTER_ROLLBACK:", len(row_items_after))
    finally:
        conn.close()

if __name__=="__main__":
    insert()
    print("==============")
    rollback()