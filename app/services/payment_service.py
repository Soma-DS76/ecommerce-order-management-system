import uuid

from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


def create_payment(customer_id: int,data: PaymentCreate,db: Session ):

    order = db.query(Order).filter( Order.id == data.order_id,Order.customer_id == customer_id ).first()

    if order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Order not found' )

    if order.payment_status == 'Paid':
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Order is already paid' )

    transaction_id = ( 'TXN-'+ uuid.uuid4().hex[:10].upper())

    payment = Payment( order_id=order.id, payment_method=data.payment_method,
        transaction_id=transaction_id, amount=order.grand_total, status='Success' )

    order.payment_status = 'Paid'

    db.add(payment)

    db.commit()

    db.refresh(payment)

    return payment


def get_customer_payment( customer_id: int, order_id: int, db: Session ):

    order = db.query(Order).filter( Order.id == order_id, Order.customer_id == customer_id ).first()

    if order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Order not found' )

    payment = db.query(Payment).filter( Payment.order_id == order_id ).first()

    if payment is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Payment not found' )

    return payment

def get_all_payments( db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(Payment).order_by( Payment.created_at.desc() ).offset(skip).limit(limit).all()