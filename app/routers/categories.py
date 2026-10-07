from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryUpdate
from app.schemas.category import CategoryResponse

from app.services.category_service import create_category
from app.services.category_service import get_categories
from app.services.category_service import get_category
from app.services.category_service import update_category
from app.services.category_service import delete_category

from app.auth.dependencies import get_current_user
from app.auth.dependencies import get_admin_user


router = APIRouter()


@router.post( '/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED )
def create( data: CategoryCreate, db: Session = Depends(get_db), 
            current_user: User = Depends(get_admin_user) ):
    return create_category(data, db)


@router.get('/', response_model=list[CategoryResponse])
def get_all( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), 
            db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    return get_categories(db, skip, limit)


@router.get( '/{category_id}', response_model=CategoryResponse )
def get_one( category_id: int, db: Session = Depends(get_db), 
             current_user: User = Depends(get_current_user) ):
    return get_category(category_id, db)


@router.put( '/{category_id}', response_model=CategoryResponse )
def update( category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), 
            current_user: User = Depends(get_admin_user) ):
    return update_category(category_id, data, db)


@router.delete('/{category_id}')
def delete( category_id: int, db: Session = Depends(get_db), 
            current_user: User = Depends(get_admin_user)):
    return delete_category(category_id, db)