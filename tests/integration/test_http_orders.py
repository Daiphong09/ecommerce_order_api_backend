import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.db.unit_of_work import UnitOfWork
class TestHTTPOrder(unittest.TestCase):
    def count_database_rows(self):
        with UnitOfWork() as uow:
            cursor = uow.cursor
            cursor.execute("SELECT COUNT(*) FROM orders AS orders_count;")
            row_orders =cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM order_items AS items_count;")
            row_items = cursor.fetchone()[0]
            return row_orders, row_items
    def cleanup_order(self, order_id):
        with UnitOfWork() as uow:
            cursor = uow.cursor
            cursor.execute("DELETE FROM order_items WHERE order_id=%s;", (order_id,))
            cursor.execute("DELETE FROM orders WHERE order_id=%s;",(order_id,))
            uow.commit()
    def test_create_order_success(self):
        request ={
        "items": [
            {"productId": "P101", "quantity": 2},
            {"productId": "P102", "quantity": 3}
        ]
        }
        client = TestClient(app)
        result = client.post("/orders", json=request)
        self.assertEqual (result.status_code ,201)
        order_id = result.json()["orderId"]
        self.addCleanup(self.cleanup_order, order_id)
        amount = result.json()["amount"]
        self.assertEqual (amount ,350000)
        order_items = result.json()["order_items"]
        self.assertEqual (len(order_items),2)    
        with UnitOfWork() as uow:
            cursor = uow.cursor
            cursor.execute("SELECT order_id FROM orders WHERE order_id=%s;",(order_id,))
            row_orders = cursor.fetchall()
            cursor.execute("SELECT order_id FROM order_items WHERE order_id=%s;",(order_id,))
            row_items = cursor.fetchall()
            self.assertEqual( len(row_orders),1)
            self.assertEqual( len(row_items),2)
        print("HTTP_STATUS:", result.status_code)
        print("AMOUNT:", result.json()["amount"])
        print("ORDER_IN_DB:", len(row_orders))
        print("ITEMS_IN_DB:", len(row_items))
        print("===========================")
    def test_product_not_found(self):
        request = {
                    "items": [
                        {"productId": "P101", "quantity": 2},
                        {"productId": "P999", "quantity": 1}
                    ]
                    }
        row_orders_before, row_items_before = self.count_database_rows()
        print("ORDER_UNCHANGE_CHECK",row_orders_before)
        print("ITEMS_UNCHANGE_CHECK:",row_items_before)
        client = TestClient(app)
        result = client.post("/orders", json=request)
        self.assertEqual (result.status_code,404)
        detail = result.json()["detail"]
        self.assertEqual (detail,"product_id P999 not found")
        row_orders_after, row_items_after = self.count_database_rows()
        test_passed = (result.status_code==404
                       and row_orders_before==row_orders_after
                       and row_items_before==row_items_after)
        test_order_passed = (row_orders_before==row_orders_after)
        test_items_passed = (row_items_before==row_items_after)
        self.assertEqual (row_orders_after,row_orders_before)
        self.assertEqual (row_items_after,row_items_before)
        print("TEST_PRODUCT_NOT_FOUND:", "PASS" if test_passed else "FAIL")
        print("HTTP_STATUS", result.status_code)
        print("ORDER_UNCHANGE_AFTER", row_orders_after,
              "TRUE" if test_order_passed else "FAIL")
        print("ITEMS_UNCHANGE_AFTER:",row_items_after,
              "TRUE" if test_items_passed else "FAIL")
        
        print("===========================")
    def test_duplicate_product(self):
        request = {
                    "items": [
                        {"productId": "P101", "quantity": 2},
                        {"productId": "P101", "quantity": 3}
                    ]
                    }
        row_orders_before, row_items_before = self.count_database_rows()
        print("ORDERS_COUNT_BEFORE:", row_orders_before)
        print("ITEMS_COUNT_BEFORE:", row_items_before)
        client = TestClient(app)
        result = client.post("/orders", json=request)
        row_orders_after, row_items_after = self.count_database_rows()
        self.assertEqual(result.status_code,422)
        details = result.json()["detail"]
        self.assertTrue(any("Duplicate product_id: P101" in detail["msg"] for detail in details))
        self.assertEqual(row_orders_after, row_orders_before)
        self.assertEqual(row_items_after, row_items_before)
        test_passed = (result.status_code==422
                       and row_orders_before==row_orders_after
                       and row_items_before==row_items_after)
        print("TEST_DUPLICATE_PRODUCT:", "PASS" if test_passed else "FAIL")
        print("HTTP_STATUS:", result.status_code)
        print("ORDER_UNCHANGE:", "TRUE" if row_orders_after==row_orders_before else "FAIL")
        print("ITEMS_UNCHANGE:", "TRUE" if row_items_after==row_items_before else "FAIL")
        print("===========================")
    def test_invalid_request_validation(self):
        requests = [("empty_items",{"items":[]}),
                   ("zero_quantity",{"items":[{"productId":"P101","quantity":0}]}),
                   ("quantity_negative",{"items":[{"productId":"P101","quantity":-1}]}),
                   ("quantity_is_string",{"items":[{"productId":"P101","quantity":"2"}]}),
                   ("quantity_true", {"items":[{"productId":"P101","quantity":True}]}),
                   ("productId_empty", {"items":[{"productId":"   ","quantity":2}]}),
                   ("not_productId", {"items":[{"quantity":2}]}),
                   ("not_quantity",{"items":[{"productId":"P101"}]})]
        for name, payload in requests:
            with self.subTest(request=name):
                client = TestClient(app)
                row_orders_before, row_items_before = self.count_database_rows()
                print("ORDER_BEFORE:", row_orders_before)
                print("ITEMS_BEFORE:", row_items_before)
                result = client.post("/orders",json=payload)
                orders_after, items_after = self.count_database_rows()
                print("ORDERS_AFTER:", orders_after)
                print("ITEMS_AFTER:", items_after)
                self.assertEqual(orders_after,row_orders_before)
                self.assertEqual(items_after,row_items_before)
                self.assertEqual(result.status_code,422)
                response = result.json()
                self.assertIn("detail", response)
                self.assertIsInstance(response["detail"], list)
                test_passed = (result.status_code==422
                               and "detail" in response
                               and isinstance(response["detail"], list)
                               and row_orders_before==orders_after
                               and row_items_before==items_after)
                print("CASE:", {name}, "PASS" if test_passed else "FAIL")
                self.assertTrue(test_passed,f"CASE_FAILED: {name}")
                
        
        
if __name__=="__main__":
    test =unittest.defaultTestLoader.loadTestsFromTestCase(TestHTTPOrder)
    result = unittest.TextTestRunner(verbosity=1).run(test)
    print("HTTP_INTEGRATION_TESTS:", 
          "PASS" if result.wasSuccessful() else "FAIL")
    if not result.wasSuccessful():
        raise SystemError()