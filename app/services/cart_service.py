from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate
from app.schemas.cart import CartItemUpdate


def get_customer_cart( customer_id: int, db: Session, skip: int = 0, limit: int = 10 ):
    cart = db.query(Cart).filter( Cart.customer_id == customer_id ).first()

    if cart is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Cart not found' )

    cart.items = cart.items[skip:skip + limit]

    return cart


def add_cart_item( customer_id: int, data: CartItemCreate, db: Session ):
    product = db.query(Product).filter( Product.id == data.product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    cart = get_customer_cart( customer_id, db )

    cart_item = db.query(CartItem).filter( CartItem.cart_id == cart.id,
                                           CartItem.product_id == data.product_id ).first()

    if cart_item is not None:
        new_quantity = cart_item.quantity + data.quantity

        if new_quantity > product.stock_quantity:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                                 detail='Requested quantity exceeds available stock')

        cart_item.quantity = new_quantity

    else:
        if data.quantity > product.stock_quantity:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                                 detail='Requested quantity exceeds available stock' )

        cart_item = CartItem( cart_id=cart.id, product_id=product.id,quantity=data.quantity )

        db.add(cart_item)

    db.commit()
    db.refresh(cart)

    return cart


def update_cart_item( customer_id: int, item_id: int,data: CartItemUpdate, db: Session ):
    cart = get_customer_cart(customer_id, db )

    cart_item = db.query(CartItem).filter( CartItem.id == item_id,CartItem.cart_id == cart.id ).first()

    if cart_item is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,detail='Cart item not found' )

    product = db.query(Product).filter(
        Product.id == cart_item.product_id,
        Product.is_active == True
    ).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Product not found')

    if data.quantity > product.stock_quantity:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, 
                             detail='Requested quantity exceeds available stock')

    cart_item.quantity = data.quantity

    db.commit()
    db.refresh(cart)

    return cart


def delete_cart_item( customer_id: int,item_id: int, db: Session ):
    cart = get_customer_cart( customer_id, db )

    cart_item = db.query(CartItem).filter( CartItem.id == item_id,CartItem.cart_id == cart.id ).first()

    if cart_item is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Cart item not found' )

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)

    return cart


def clear_cart( customer_id: int,db: Session ):
    cart = get_customer_cart( customer_id, db )

    for item in cart.items:
        db.delete(item)

    db.commit()
    db.refresh(cart)

    return { 'message': 'Cart cleared successfully' }