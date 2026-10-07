from fastapi import APIRouter
from fastapi import Depends
from fastapi import BackgroundTasks

from sqlalchemy.orm import Session

from app.auth.dependencies import get_admin_user
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderResponse
from app.schemas.admin_order import OrderStatusUpdate
from app.services.order_service import get_all_orders
from app.services.order_service import update_order_status
from app.services.email_service import send_order_status_email
from fastapi import Query

router = APIRouter()

@router.get('/', response_model=list[OrderResponse])
def get_orders( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                current_user: User = Depends(get_admin_user), db: Session = Depends(get_db) ):
    return get_all_orders(db, skip, limit)


@router.put('/{order_id}/status', response_model=OrderResponse)
def change_order_status( order_id: int, data: OrderStatusUpdate,
                         background_tasks: BackgroundTasks, current_user: User = Depends(get_admin_user),
                         db: Session = Depends(get_db) ):
    order = update_order_status(order_id, data.status, db)

    background_tasks.add_task( send_order_status_email, order.customer.email, order.order_number, order.status )

    return order