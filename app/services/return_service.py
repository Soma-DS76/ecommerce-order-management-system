from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.return_order import ReturnOrder
from app.schemas.return_order import ReturnCreate
from app.schemas.return_order import ReturnStatusUpdate


def create_return( customer_id: int, data: ReturnCreate, db: Session ):

    order = db.query(Order).filter( Order.id == data.order_id, Order.customer_id == customer_id ).first()

    if order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Order not found' )

    if order.status != 'Delivered':
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, 
                             detail='Only delivered orders can be returned' )

    existing_return = db.query(ReturnOrder).filter( ReturnOrder.order_id == data.order_id ).first()

    if existing_return is not None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Return already requested for this order' )

    return_order = ReturnOrder( order_id=order.id, reason=data.reason,
                                status='Requested', refund_amount=order.grand_total )

    db.add(return_order)

    db.commit()

    db.refresh(return_order)

    return return_order


def get_customer_returns( customer_id: int, db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(ReturnOrder).join( Order, ReturnOrder.order_id == Order.id ).filter(
           Order.customer_id == customer_id ).order_by( ReturnOrder.created_at.desc() 
                                                      ).offset(skip).limit(limit).all()


def get_customer_return( customer_id: int, return_id: int, db: Session ):

    return_order = db.query(ReturnOrder).join( Order, ReturnOrder.order_id == Order.id ).filter( 
                   ReturnOrder.id == return_id, Order.customer_id == customer_id ).first()

    if return_order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Return not found' )
    return return_order

def get_all_returns( db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(ReturnOrder).order_by( ReturnOrder.created_at.desc() ).offset(skip).limit(limit).all()


def update_return_status( return_id: int, data: ReturnStatusUpdate, db: Session ):

    return_order = db.query(ReturnOrder).filter( ReturnOrder.id == return_id ).first()

    if return_order is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Return not found')

    valid_statuses = [ 'Approved', 'Rejected','Refunded' ]

    if data.status not in valid_statuses:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid return status' )

    if data.status == 'Rejected':
        if data.rejection_reason is None:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                                 detail='Rejection reason is required' )

        return_order.rejection_reason = data.rejection_reason

    if data.status == 'Approved':
        return_order.rejection_reason = None

    if data.status == 'Refunded':
        return_order.rejection_reason = None

    return_order.status = data.status

    db.commit()

    db.refresh(return_order)

    return return_order