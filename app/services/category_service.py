from fastapi import HTTPException
from fastapi import status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryUpdate


def create_category(data: CategoryCreate, db: Session):
    old_category = db.query(Category).filter( Category.name == data.name ).first()

    if old_category is not None:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT,detail='Category already exists' )

    category = Category( name=data.name, is_active=True )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    except IntegrityError:
        db.rollback()

        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Category already exists' )


def get_categories(db: Session):
    categories = db.query(Category).filter( Category.is_active == True ).all()

    return categories


def get_category(category_id: int, db: Session):
    category = db.query(Category).filter( Category.id == category_id, Category.is_active == True ).first()

    if category is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    return category


def update_category( category_id: int, data: CategoryUpdate, db: Session ):
    category = db.query(Category).filter( Category.id == category_id, Category.is_active == True ).first()

    if category is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    old_category = db.query(Category).filter( Category.name == data.name, Category.id != category_id ).first()

    if old_category is not None:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Category already exists' )

    category.name = data.name

    try:
        db.commit()
        db.refresh(category)

        return category

    except IntegrityError:
        db.rollback()
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Category already exists' )


def delete_category(category_id: int, db: Session):
    category = db.query(Category).filter( Category.id == category_id, Category.is_active == True ).first()

    if category is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    active_product = None

    for product in category.products:
        if product.is_active is True:
            active_product = product
            break

    if active_product is not None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Cannot delete category with active products' )

    category.is_active = False

    db.commit()

    return { 'message': 'Category deleted successfully' }