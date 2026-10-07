from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    sku: str = Field(min_length=2, max_length=100)
    description: str | None = None
    category_id: int
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    sku: str = Field(min_length=2, max_length=100)
    description: str | None = None
    category_id: int
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    description: str | None
    category_id: int
    price: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime