from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.user import User
from app.models.product import Product


def get_sales_report(db: Session):
    orders = db.query(Order).all()

    total_orders = len(orders)

    total_sales = 0

    pending_orders = 0
    confirmed_orders = 0
    shipped_orders = 0
    delivered_orders = 0
    cancelled_orders = 0

    for order in orders:
        if order.status != 'Cancelled':
            total_sales = total_sales + order.grand_total

        if order.status == 'Pending':
            pending_orders = pending_orders + 1
        elif order.status == 'Confirmed':
            confirmed_orders = confirmed_orders + 1
        elif order.status == 'Shipped':
            shipped_orders = shipped_orders + 1
        elif order.status == 'Delivered':
            delivered_orders = delivered_orders + 1
        elif order.status == 'Cancelled':
            cancelled_orders = cancelled_orders + 1

    total_customers = db.query(User).filter(User.role == 'Customer').count()

    total_products = db.query(Product).count()

    low_stock_products = db.query(Product).filter( Product.stock_quantity <= 5, Product.is_active == True ).count()

    return { 'total_orders': total_orders, 'total_sales': total_sales, 'pending_orders': pending_orders,
            'confirmed_orders': confirmed_orders, 'shipped_orders': shipped_orders,
            'delivered_orders': delivered_orders, 'cancelled_orders': cancelled_orders,
            'total_customers': total_customers, 'total_products': total_products, 
            'low_stock_products': low_stock_products }