from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_customer_user
from app.database import get_db
from app.models.user import User
from app.schemas.address import AddressCreate
from app.schemas.address import AddressUpdate
from app.schemas.address import AddressResponse
from app.services.address_service import create_address
from app.services.address_service import get_customer_addresses
from app.services.address_service import get_address
from app.services.address_service import update_address
from app.services.address_service import delete_address

from fastapi import Query


router = APIRouter()


@router.post( '/', response_model=AddressResponse, status_code=status.HTTP_201_CREATED )
def create( data: AddressCreate,current_user: User = Depends(get_customer_user),db: Session = Depends(get_db)):
    return create_address( current_user.id, data, db )


@router.get('/', response_model=list[AddressResponse])
def get_addresses( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), 
                   current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ):
    return get_customer_addresses( current_user.id, db, skip, limit )


@router.get( '/{address_id}', response_model=AddressResponse )
def get_one( address_id: int, current_user: User = Depends(get_customer_user), db: Session = Depends(get_db)):
    return get_address( current_user.id, address_id, db)


@router.put( '/{address_id}', response_model=AddressResponse )
def update( address_id: int,data: AddressUpdate, current_user: User = Depends(get_customer_user),
            db: Session = Depends(get_db)):
    return update_address( current_user.id, address_id, data, db )


@router.delete('/{address_id}')
def delete( address_id: int, current_user: User = Depends(get_customer_user),
            db: Session = Depends(get_db) ):
    return delete_address( current_user.id, address_id, db )