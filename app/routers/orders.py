from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_customer_user
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate
from app.schemas.order import OrderResponse
from app.services.order_service import create_order
from app.services.order_service import get_customer_orders
from app.services.order_service import get_customer_order
from fastapi import BackgroundTasks
from app.services.email_service import send_order_email

from fastapi import Query

router = APIRouter()


@router.post('/', response_model=OrderResponse, status_code=status.HTTP_201_CREATED )
def create( data: OrderCreate, background_tasks: BackgroundTasks, 
            current_user: User = Depends(get_customer_user),db: Session = Depends(get_db) ):

    order = create_order( current_user.id, data, db )
    background_tasks.add_task( send_order_email,current_user.email, order.order_number, str(order.grand_total))

    return order


@router.get('/', response_model=list[OrderResponse])
def get_orders( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), 
                current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ):
    return get_customer_orders( current_user.id, db, skip, limit )

@router.get( '/{order_id}', response_model=OrderResponse )
def get_one_order( order_id: int, current_user: User = Depends(get_customer_user),db: Session = Depends(get_db)):
    return get_customer_order( current_user.id, order_id, db )