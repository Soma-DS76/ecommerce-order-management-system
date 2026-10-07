from datetime import datetime
import uuid
from decimal import Decimal

from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.address import Address
from app.models.cart import Cart
from app.models.order import Order
from app.models.order import OrderItem
from app.schemas.order import OrderCreate


def create_order( customer_id: int, data: OrderCreate, db: Session):

    address = db.query(Address).filter( Address.id == data.address_id, 
                                        Address.customer_id == customer_id ).first()

    if address is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Address not found' )

    cart = db.query(Cart).filter( Cart.customer_id == customer_id ).first()

    if cart is None or len(cart.items) == 0:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Cart is empty' )

    subtotal = Decimal('0.00')

    for cart_item in cart.items:

        product = cart_item.product

        if product.is_active is False:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Product is not available')

        if cart_item.quantity > product.stock_quantity:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Product stock is not available' )

        subtotal = subtotal + ( product.price * cart_item.quantity)

    tax_amount = subtotal * Decimal('0.18')

    delivery_charge = Decimal('50.00')

    grand_total = ( subtotal + tax_amount + delivery_charge )

    order_number = ( 'ORD-' + uuid.uuid4().hex[:8].upper() )

    order = Order( order_number=order_number, customer_id=customer_id,
                   address_id=data.address_id, subtotal=subtotal, tax_amount=tax_amount,
                   delivery_charge=delivery_charge, grand_total=grand_total, status='Pending',
                   payment_status='Unpaid' )

    db.add(order)

    db.flush()

    for cart_item in cart.items:

        product = cart_item.product

        line_total = ( product.price * cart_item.quantity )

        order_item = OrderItem( order_id=order.id, product_id=product.id, quantity=cart_item.quantity, 
                                unit_price=product.price, line_total=line_total )

        product.stock_quantity = ( product.stock_quantity - cart_item.quantity )

        db.add(order_item)

    for cart_item in list(cart.items):
        db.delete(cart_item)

    db.commit()

    db.refresh(order)

    return order


def get_customer_orders( customer_id: int, db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(Order).filter( Order.customer_id == customer_id 
                                  ).order_by( Order.created_at.desc()
                                             ).offset(skip).limit(limit).all()


def get_customer_order( customer_id: int, order_id: int, db: Session ):

    order = db.query(Order).filter( Order.id == order_id, Order.customer_id == customer_id ).first()

    if order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Order not found' )

    return order

def get_all_orders( db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(Order).order_by( Order.created_at.desc() ).offset(skip).limit(limit).all()


def update_order_status( order_id: int,new_status: str, db: Session ):
 
    order = db.query(Order).filter( Order.id == order_id ).first()

    if order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Order not found' )

    valid_statuses = [ 'Pending', 'Confirmed','Shipped', 'Delivered', 'Cancelled' ]

    if new_status not in valid_statuses:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid order status' )

    order.status = new_status

    if new_status == 'Delivered':
        order.delivered_at = datetime.utcnow()

    db.commit()

    db.refresh(order)

    return order