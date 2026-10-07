from decimal import Decimal
from pydantic import BaseModel


class SalesReportResponse(BaseModel):
    total_orders: int
    total_sales: Decimal
    pending_orders: int
    confirmed_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_customers: int
    total_products: int
    low_stock_products: int