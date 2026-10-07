from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str = Field(min_length=2, max_length=30)


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    payment_method: str
    transaction_id: str
    amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime