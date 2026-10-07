from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_customer_user
from app.database import get_db
from app.models.user import User
from app.schemas.return_order import ReturnCreate
from app.schemas.return_order import ReturnResponse
from app.services.return_service import create_return
from app.services.return_service import get_customer_returns
from app.services.return_service import get_customer_return
from fastapi import Query


router = APIRouter()


@router.post( '/', response_model=ReturnResponse, status_code=status.HTTP_201_CREATED )
def request_return( data: ReturnCreate, current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ):
    return create_return( current_user.id, data, db )


@router.get('/', response_model=list[ReturnResponse])
def get_returns( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                 current_user: User = Depends(get_customer_user), db: Session = Depends(get_db)):
    return get_customer_returns( current_user.id, db, skip, limit )


@router.get('/{return_id}', response_model=ReturnResponse )
def get_one_return( return_id: int, current_user: User = Depends(get_customer_user), 
                    db: Session = Depends(get_db) ):
    return get_customer_return( current_user.id,return_id,db )