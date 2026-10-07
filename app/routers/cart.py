from decimal import Decimal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_customer_user
from app.database import get_db
from app.models import cart
from app.models.user import User
from app.schemas.cart import CartItemCreate
from app.schemas.cart import CartItemUpdate
from app.schemas.cart import CartResponse
from app.services.cart_service import add_cart_item
from app.services.cart_service import update_cart_item
from app.services.cart_service import delete_cart_item
from app.services.cart_service import clear_cart
from app.services.cart_service import get_customer_cart
from fastapi import Query

router = APIRouter()


def create_cart_response(cart):
    items = []
    total_amount = Decimal('0.00')

    for item in cart.items:
        price = item.product.price
        total_price = price * item.quantity

        items.append({ 'id': item.id, 'product_id': item.product_id, 'product_name': item.product.name,
            'quantity': item.quantity, 'price': price, 'total_price': total_price,
            'created_at': item.created_at,'updated_at': item.updated_at })

        total_amount = total_amount + total_price

    return { 'id': cart.id, 'customer_id': cart.customer_id,'items': items, 
             'total_amount': total_amount, 'created_at': cart.created_at,
             'updated_at': cart.updated_at }


@router.post('/items',response_model=CartResponse,status_code=status.HTTP_201_CREATED)
def add_item(data: CartItemCreate, current_user: User = Depends(get_customer_user),db: Session = Depends(get_db) ):
    cart = add_cart_item( current_user.id, data,db )

    return create_cart_response(cart)


@router.get('/', response_model=CartResponse)
def get_cart( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), 
             current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ):
    return get_customer_cart( current_user.id, db, skip, limit )


@router.put( '/items/{item_id}', response_model=CartResponse )
def update_item( item_id: int, data: CartItemUpdate, 
                 current_user: User = Depends(get_customer_user),db: Session = Depends(get_db)):
    cart = update_cart_item(current_user.id,item_id, data,db )
    return create_cart_response(cart)


@router.delete( '/items/{item_id}', response_model=CartResponse )
def delete_item( item_id: int,current_user: User = Depends(get_customer_user),
                 db: Session = Depends(get_db) ):
    
    cart = delete_cart_item( current_user.id, item_id, db )
    return create_cart_response(cart)


@router.delete( '/', status_code=status.HTTP_200_OK )
def delete_cart( current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ):
    return clear_cart( current_user.id, db )