from app.db.unit_of_work import UnitOfWork
from dotenv import load_dotenv
from app.orders.repository import insert_order_items, insert_order
from uuid import uuid4
def test_uow():
    load_dotenv()
    order_id =f"ORD-{uuid4()}"
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
    with UnitOfWork() as uow:
        cursor = uow.cursor
        insert_order(cursor, order_id, total_amount)
        insert_order_items(cursor, order_id, order_items)
        cursor.execute("""SELECT order_id FROM orders 
            WHERE order_id=%s;""", (order_id,))
        row_orders = cursor.fetchall()
        assert len(row_orders) ==1
        cursor.execute("""SELECT order_id FROM order_items
                WHERE order_id=%s;""",(order_id,))
        row_items = cursor.fetchall()
        assert len(row_items) ==2
        uow.commit()
        print("ORDER_IN_TX:", len(row_orders))
        print("ITEMS_IN_TX:", len(row_items))

        print("COMMIT_SUCCESS")
    with UnitOfWork() as uow:
        
        cursor = uow.cursor
        cursor.execute("""SELECT order_id FROM orders 
            WHERE order_id=%s;""", (order_id,))
        order_after_commit = cursor.fetchall()
        assert len(order_after_commit) ==1
        cursor.execute("""SELECT order_id FROM order_items 
            WHERE order_id=%s;""",(order_id,))
        items_after_commit = cursor.fetchall()
        assert len(items_after_commit) ==2
        print("ORDER_AFTER_COMMIT:", len(order_after_commit))
        print("ITEMS_AFTER_COMMIT:", len(items_after_commit))
if __name__=="__main__":
    test_uow()