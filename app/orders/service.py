from app.products.repository import get_product_rows
from app.orders.repository import insert_order, insert_order_items
class ProductNotFound(ValueError):
    pass
def prepare_order(cursor, items):
    product_ids_seen = set()
    product_ids = []
    for item in items:
        product_id = item.get("productId")
        if product_id not in product_ids_seen:
            product_ids_seen.add(product_id)
            product_ids.append(product_id)
    products=get_product_rows(cursor, product_ids)
    product_map = {}
    for row in products:
        product_map[row[0]] = row[1]
    for product_id in product_ids:
        if product_id not in product_map:
            raise ProductNotFound(f"product_id {product_id} not found")
    amount =0
    order_items = []
    for item in items:
        product_id = item.get("productId")
        quantity = item.get("quantity")
        unit_price = product_map[product_id]
        subtotal = quantity*unit_price
        order_items.append({"product_id":product_id, 
                       "quantity":quantity,
                       "unit_price":unit_price,
                       "subtotal":subtotal})    
        amount +=subtotal   
    return {"order_items":order_items, "amount":amount}
def create_order(cursor, order_id, items):
    prepare = prepare_order(cursor, items)
    amount = prepare["amount"]
    order_items = prepare["order_items"]
    insert_order(cursor, order_id, amount)
    insert_order_items(cursor, order_id, order_items)
    return {"order_id":order_id, "amount":amount,
            "order_items":order_items}

        