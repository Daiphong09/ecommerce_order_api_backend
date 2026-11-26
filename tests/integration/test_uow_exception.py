from dotenv import load_dotenv
from app.db.unit_of_work import UnitOfWork
from app.orders.repository import insert_order, insert_order_items

def test_exception(): 
    load_dotenv()
    order_id = "ORD-RB05-UOW-EXCEPTION-001"
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
        print("BEFORE")
        with UnitOfWork() as uow:
            cursor = uow.cursor
            insert_order(cursor, order_id, total_amount)
            insert_order_items(cursor, order_id, order_items)
            cursor.execute("SELECT order_id FROM orders WHERE order_id=%s;",(order_id,))
            before_orders = cursor.fetchall()
            cursor.execute("SELECT order_id FROM order_items WHERE order_id=%s;",(order_id,))
            before_items = cursor.fetchall()
            assert len(before_orders) ==1
            assert len(before_items) ==2
            print("RUNTIME: BEFORE EXCEPTION")
            print("ORDERS_IN_TX:", len(before_orders))
            print("ITEMS_IN_TX:", len(before_items))
            raise RuntimeError("SIMULATED_FAILURE")
    except RuntimeError as e:
        assert str(e) == "SIMULATED_FAILURE"
        print("RUNTIME_ERROR:", str(e))
    else:
        raise AssertionError("Expected RUNTIME_ERROR: SIMULATED_FAILURE but no exception was raised")

    print("=======================")
    print("AFTER_RUNTIME_ERROR")
    with UnitOfWork() as uow:
        cursor = uow.cursor
        cursor.execute("SELECT order_id FROM orders WHERE order_id=%s;",(order_id,))
        after_orders = cursor.fetchall()
        cursor.execute("SELECT order_id FROM order_items WHERE order_id=%s;",(order_id,))
        after_items = cursor.fetchall()
        assert len(after_orders) ==0
        assert len(after_items) ==0
        print("ORDER_AFTER_ROLLBACK:", len(after_orders))
        print("ITEMS_AFTER_ROLLBACK:", len(after_items))

if __name__=="__main__":
    print("START")
    try:
        test_exception()
    except Exception as e:
        print("TEST_UOW_EXCEPTION: FAIL")
        print("ERROR:", repr(e))
        raise
    else:
        print("TEST_UOW_EXCEPTION: PASS")