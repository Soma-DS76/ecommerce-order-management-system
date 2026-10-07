from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate
from app.schemas.address import AddressUpdate


def get_customer_addresses( customer_id: int, db: Session, skip: int = 0, limit: int = 10 ):
    return db.query(Address).filter( Address.customer_id == customer_id 
                                    ).order_by( Address.created_at.desc() 
                                               ).offset(skip).limit(limit).all()


def get_address( customer_id: int, address_id: int, db: Session ):
    address = db.query(Address).filter( Address.id == address_id, Address.customer_id == customer_id ).first()

    if address is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Address not found' )

    return address


def create_address( customer_id: int,data: AddressCreate, db: Session ):
    if data.is_default is True:
        old_default = db.query(Address).filter( Address.customer_id == customer_id, 
                                                Address.is_default == True ).all()

        for address in old_default:
            address.is_default = False

    address = Address( customer_id=customer_id, full_name=data.full_name, phone=data.phone,
        address_line=data.address_line, city=data.city, state=data.state, pincode=data.pincode, 
        is_default=data.is_default )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address


def update_address( customer_id: int,address_id: int, data: AddressUpdate,  db: Session ):
    address = db.query(Address).filter( Address.id == address_id, Address.customer_id == customer_id ).first()

    if address is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Address not found' )

    if data.is_default is True:
        old_default = db.query(Address).filter( Address.customer_id == customer_id, Address.id != address_id, 
                                                Address.is_default == True ).all()

        for old_address in old_default:
            old_address.is_default = False

    address.full_name = data.full_name
    address.phone = data.phone
    address.address_line = data.address_line
    address.city = data.city
    address.state = data.state
    address.pincode = data.pincode
    address.is_default = data.is_default

    db.commit()
    db.refresh(address)

    return address


def delete_address( customer_id: int, address_id: int, db: Session ):
    address = db.query(Address).filter( Address.id == address_id, Address.customer_id == customer_id ).first()

    if address is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Address not found' )

    db.delete(address)
    db.commit()

    return { 'message': 'Address deleted successfully' }