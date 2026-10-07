from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_admin_user
from app.auth.dependencies import get_customer_user

from app.database import get_db

from app.models.user import User

from app.schemas.payment import PaymentCreate
from app.schemas.payment import PaymentResponse

from app.services.payment_service import create_payment
from app.services.payment_service import get_customer_payment
from app.services.payment_service import get_all_payments


router = APIRouter()


@router.post( '/', response_model=PaymentResponse, status_code=status.HTTP_201_CREATED )
def make_payment( data: PaymentCreate,current_user: User = Depends(get_customer_user),
                  db: Session = Depends(get_db)):
    return create_payment(current_user.id, data, db)


@router.get('/', response_model=list[PaymentResponse])
def get_payments( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                  current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return get_all_payments(db, skip, limit)