from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import get_admin_user
from app.database import get_db
from app.models.user import User
from app.schemas.return_order import ReturnResponse
from app.schemas.return_order import ReturnStatusUpdate
from app.services.return_service import get_all_returns
from app.services.return_service import update_return_status
from fastapi import Query


router = APIRouter()


@router.get('/', response_model=list[ReturnResponse])
def get_returns( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), current_user: User = Depends(get_admin_user),
                 db: Session = Depends(get_db)):
    return get_all_returns(db, skip, limit)


@router.put( '/{return_id}/status', response_model=ReturnResponse )
def change_return_status( return_id: int, data: ReturnStatusUpdate,
                          current_user: User = Depends(get_admin_user), db: Session = Depends(get_db) ):
    return update_return_status( return_id, data, db )