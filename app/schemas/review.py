from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field( ge=1, le=5 )
    comment: str | None = Field( default=None, max_length=1000 )


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    customer_id: int
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime


class ReviewUpdate(BaseModel):
    rating: int = Field( ge=1, le=5 )
    comment: str | None = Field( default=None, max_length=1000 )