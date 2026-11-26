from app.db.db_connection import get_connection
from app.orders.service import prepare_order, ProductNotFound
from dotenv import load_dotenv
load_dotenv()
def success():
    items = [
    {"productId": "P101", "quantity": 2},
    {"productId": "P102", "quantity": 3}
]   
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            prepared =prepare_order(cursor, items)
            amount = prepared["amount"]
            order_items = prepared["order_items"]
            assert amount ==350000
            assert len(order_items) ==2
            subtotals = {}
            for order in order_items:
                product_id = order["product_id"]
                subtotal = order["subtotal"]
                subtotals[product_id] = subtotal
            assert subtotals["P101"] ==200000
            assert subtotals["P102"] == 150000
            print("PREPARE_ORDER_SUCCESS")
            print("AMOUNT:", amount)
            print("ORDER_ITEMS_COUNT:", len(order_items))
            print("P101_SUBTOTAL:", subtotals["P101"])
            print("P102_SUBTOTAL:", subtotals["P102"])
    finally:
        conn.close()

def invalid():
    items = [
    {"productId": "P101", "quantity": 2},
    {"productId": "P999", "quantity": 1}
]
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            prepare_order(cursor, items)
    except ProductNotFound as e:
        assert "P999" in str(e)
        print("EXPECTED_ERROR:", e)
    else:
        raise AssertionError("Expected ProductNotFound but no exception was raised")
    finally:
        conn.close()
if __name__=="__main__":
    success()
    invalid()