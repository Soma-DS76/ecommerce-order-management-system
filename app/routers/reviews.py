from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.dependencies import get_customer_user
from app.database import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewResponse
from app.schemas.review import ReviewUpdate
from app.services.review_service import create_review
from app.services.review_service import get_product_reviews
from app.services.review_service import get_customer_reviews
from app.services.review_service import get_customer_review
from app.services.review_service import update_review
from app.services.review_service import delete_review
from fastapi import Query


router = APIRouter()


@router.post( '/', response_model=ReviewResponse, status_code=status.HTTP_201_CREATED )
def add_review(data: ReviewCreate, current_user: User = Depends(get_customer_user),db: Session = Depends(get_db)):
    return create_review( current_user.id, data, db )


@router.get( '/product/{product_id}', response_model=list[ReviewResponse])
def get_product_review_list( product_id: int, skip: int = Query(0, ge=0), 
                            limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):

    return get_product_reviews(product_id, db, skip, limit)


@router.get('/', response_model=list[ReviewResponse])
def get_reviews( skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                 current_user: User = Depends(get_customer_user),db: Session = Depends(get_db) ):

    return get_customer_reviews(current_user.id, db, skip, limit)


@router.get( '/{review_id}',response_model=ReviewResponse )
def get_one_review( review_id: int, current_user: User = Depends(get_customer_user),
                    db: Session = Depends(get_db) ):
    return get_customer_review( current_user.id, review_id, db )


@router.put( '/{review_id}', response_model=ReviewResponse)
def edit_review( review_id: int, data: ReviewUpdate, current_user: User = Depends(get_customer_user),
                 db: Session = Depends(get_db)):
    return update_review( current_user.id,review_id,data,db )


@router.delete( '/{review_id}' )
def remove_review( review_id: int, current_user: User = Depends(get_customer_user), db: Session = Depends(get_db) ): 
    return delete_review( current_user.id, review_id, db )