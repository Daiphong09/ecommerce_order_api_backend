from fastapi import FastAPI, Query, HTTPException
from app.db.db_connection import get_connection
from app.products.repository import get_product_rows
from app.orders.service import create_order, ProductNotFound
from dotenv import load_dotenv
from typing import Annotated
from app.orders.schemas import CreateOrderRequest
from uuid import uuid4
from app.db.unit_of_work import UnitOfWork
load_dotenv()
app = FastAPI()
@app.get("/health")
def health():
    return {"status":"ok",
            "service":"ecommerce-api"}
@app.post("/orders/validate")
def validate_orders(payload:CreateOrderRequest):
    return {"valid":True, "item_count":len(payload.items)}
@app.get("/products")
def get_products(product_ids:Annotated[list[str],Query()]):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            rows =get_product_rows(cursor, product_ids)
            results = []
            for row in rows:
                product = {"productId":row[0],
                           "productCost":row[1]}
                results.append(product)
        return {"products":results}
    finally:
        conn.close()
@app.post("/orders", status_code=201)
def create_order_endpoint(payload:CreateOrderRequest):
    items = payload.model_dump()["items"]
    order_id = f"ORD-{uuid4()}"
    try:
        with UnitOfWork() as uow:
            cursor = uow.cursor
            response =create_order(cursor, order_id,items)
            uow.commit()
            order_id = response["order_id"]
            amount = response["amount"]
            order_items = response["order_items"]
            return {"orderId":order_id,
                    "amount":amount,
                    "order_items":order_items}
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    