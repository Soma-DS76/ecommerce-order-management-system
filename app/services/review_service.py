from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order import OrderItem
from app.models.product import Product
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewUpdate


def create_review( customer_id: int, data: ReviewCreate, db: Session ):

    product = db.query(Product).filter( Product.id == data.product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    purchased = db.query(OrderItem).join( Order, OrderItem.order_id == Order.id ).filter( 
                Order.customer_id == customer_id, OrderItem.product_id == data.product_id,
                Order.status == 'Delivered').first()

    if purchased is None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='You can review only purchased products')

    existing_review = db.query(Review).filter( Review.product_id == data.product_id,
                                               Review.customer_id == customer_id).first()

    if existing_review is not None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, 
                             detail='You have already reviewed this product' )

    review = Review( product_id=data.product_id, customer_id=customer_id, 
                     rating=data.rating, comment=data.comment )

    db.add(review)

    db.commit()

    db.refresh(review)

    return review


def get_product_reviews(product_id: int, db: Session):
    product = db.query(Product).filter( Product.id == product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    reviews = db.query(Review).filter( Review.product_id == product_id ).order_by( Review.created_at.desc() ).all()

    return reviews


def get_customer_reviews(customer_id: int, db: Session, skip: int = 0, limit: int = 10 ):

    reviews = db.query(Review).filter( Review.customer_id == customer_id 
                                      ).order_by( Review.created_at.desc() 
                                      ).offset(skip).limit(limit).all()

    return reviews


def get_customer_review( customer_id: int, review_id: int, db: Session ):

    review = db.query(Review).filter( Review.id == review_id, Review.customer_id == customer_id ).first()

    if review is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Review not found' )

    return review


def update_review( customer_id: int, review_id: int, data: ReviewUpdate, db: Session ):

    review = db.query(Review).filter( Review.id == review_id, Review.customer_id == customer_id ).first()

    if review is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Review not found' )

    review.rating = data.rating
    review.comment = data.comment

    db.commit()

    db.refresh(review)

    return review


def delete_review( customer_id: int, review_id: int, db: Session ):

    review = db.query(Review).filter( Review.id == review_id, Review.customer_id == customer_id ).first()

    if review is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Review not found' )

    db.delete(review)

    db.commit()

    return { 'message': 'Review deleted successfully' }