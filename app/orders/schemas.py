from pydantic import BaseModel, Field, field_validator
class OrderItemRequest(BaseModel):
    productId: str = Field(min_length=1,)
    quantity: int = Field(gt=0, strict=True)
    @field_validator("productId")
    @classmethod
    def validate_product(cls, value:str) -> str:
        if value.strip()=="":
            raise ValueError("productId not be empty")
        return value
class CreateOrderRequest(BaseModel):
    items: list[OrderItemRequest] = Field(min_length=1)
    @field_validator("items")
    @classmethod
    def validate_product_id(cls, items:list[OrderItemRequest]) -> list[OrderItemRequest]:
        product_seen = set()
        for item in items:
            product_id = item.productId
            if product_id in product_seen:
                raise ValueError(f"Duplicate product_id: {item.productId}")
            product_seen.add(product_id)
        return items