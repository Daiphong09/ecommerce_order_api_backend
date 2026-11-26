from dotenv import load_dotenv
from app.orders.service import create_order, ProductNotFound
from app.db.unit_of_work import UnitOfWork

def create_order_success():
    load_dotenv()
    print("CREATE_ORDER_SUCCESS")
    order_id = "ORD-RB06-SERVICE-001"

    items = [
        {"productId": "P101", "quantity": 2},
        {"productId": "P102", "quantity": 3}
    ]
    with UnitOfWork() as uow:
        cursor = uow.cursor
        result =create_order(cursor, order_id, items)
        assert result["amount"] == 350000
        cursor.execute("SELECT order_id FROM orders WHERE order_id=%s;",(order_id,))
        row_orders = cursor.fetchall()
        cursor.execute("SELECT order_id FROM order_items WHERE order_id=%s;",(order_id,))
        row_items= cursor.fetchall()
        assert len(result["order_items"]) == 2
        assert len(row_orders) == 1
        assert len(row_items) ==2
        print("AMOUNT:", result["amount"])
        print("ORDERS_IN_TX:", len(row_orders))
        print("ITEMS_IN_TX:", len(row_items))
def invalid_product():
    load_dotenv()
    print("INVALID_PRODUCT")
    order_id = "ORD-RB06-SERVICE-INVALID-001"
    items = [
        {"productId": "P101", "quantity": 2},
        {"productId": "P999", "quantity": 1}
    ]
    try:
        with UnitOfWork() as uow:
            cursor = uow.cursor
            create_order(cursor,order_id, items)
    except ProductNotFound as e:
        assert str(e) == f"product_id P999 not found"
        print("EXPECTED_ERROR:", str(e))
    else:
        raise AssertionError("Expected ProductNotFound, but no exception was raised")
    print("VERIFICATION: Order_id ORD-RB06-SERVICE-INVALID-001 not save")
    with UnitOfWork() as uow:
        cursor = uow.cursor
        cursor.execute("""SELECT order_id FROM orders WHERE order_id=%s;""",(order_id,))
        row_orders = cursor.fetchall()
        cursor.execute("""SELECT order_id FROM order_items WHERE order_id=%s;""",(order_id,))
        row_items = cursor.fetchall()
        print("POSTGRESQL_NO_COMMIT: ORD-RB06-SERVICE-INVALID-001")
        assert len(row_orders) ==0
        assert len(row_items) ==0
        print("ORDERS_AFTER_ERROR:", len(row_orders))
        print("ITEMS_AFTE_ERROR:", len(row_items))

if __name__=="__main__":
    create_order_success()
    print("================")
    try:
        invalid_product()
    except Exception as e:
        print("TEST_INVALID_PRODUCT: FAIL")
        print("ERROR_EXCEPTION:", repr(e))
        raise
    else:
        print("TEST_INVALID_PRODUCT: PASS")
