from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import ConfigDict


class OrderCreate(BaseModel):
    address_id: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_id: int
    address_id: int
    subtotal: Decimal
    tax_amount: Decimal
    delivery_charge: Decimal
    grand_total: Decimal
    status: str
    payment_status: str
    delivered_at: datetime | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]