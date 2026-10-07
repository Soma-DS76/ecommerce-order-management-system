from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_admin_user
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate
from app.schemas.product import ProductResponse
from app.schemas.product import ProductUpdate
from app.services.product_service import create_product
from app.services.product_service import delete_product
from app.services.product_service import get_product
from app.services.product_service import get_products
from app.services.product_service import update_product

from decimal import Decimal
from fastapi import Query



router = APIRouter()


@router.post('/',response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
def create(data: ProductCreate,db: Session = Depends(get_db),current_user: User = Depends(get_admin_user)):
    return create_product(data, db)


@router.get('/', response_model=list[ProductResponse])
def get_all_products( name: str = None, category_id: int = None,
    min_price: Decimal = None, max_price: Decimal = None, in_stock: bool = None,
    sort_by: str = 'created_at', order: str = 'desc', skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db) ):
    return get_products( db, name, category_id, min_price, max_price, in_stock, 
                         sort_by, order, skip, limit )


@router.get('/{product_id}',response_model=ProductResponse)
def get_one( product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_product(product_id, db)


@router.put( '/{product_id}',response_model= ProductResponse )
def update( product_id: int,data: ProductUpdate,
           db: Session = Depends(get_db),current_user: User = Depends(get_admin_user) ):
    return update_product( product_id,data, db )


@router.delete( '/{product_id}')
def delete( product_id: int,db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    return delete_product( product_id, db )