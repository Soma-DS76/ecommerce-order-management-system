from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class ReturnCreate(BaseModel):
    order_id: int
    reason: str = Field( min_length=5, max_length=500 )


class ReturnResponse(BaseModel):
    id: int
    order_id: int
    reason: str
    status: str
    refund_amount: Decimal | None
    rejection_reason: str | None
    created_at: datetime
    updated_at: datetime


class ReturnStatusUpdate(BaseModel):
    status: str
    rejection_reason: str | None = None