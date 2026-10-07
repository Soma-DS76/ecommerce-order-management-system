from fastapi import HTTPException
from fastapi import status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate

from decimal import Decimal




def create_product(data: ProductCreate, db: Session):
    category = db.query(Category).filter( Category.id == data.category_id, Category.is_active == True ).first()

    if category is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    old_product = db.query(Product).filter( Product.sku == data.sku ).first()

    if old_product is not None:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='SKU already exists' )

    product = Product( name=data.name,sku=data.sku,description=data.description,
                       category_id=data.category_id,price=data.price,stock_quantity=data.stock_quantity,
                       is_active=True )

    try:
        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    except IntegrityError:
        db.rollback()

        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='SKU already exists' )


def get_products( db: Session, name: str = None, category_id: int = None,
                  min_price: Decimal = None, max_price: Decimal = None, in_stock: bool = None, 
                  sort_by: str = 'created_at', order: str = 'desc', skip: int = 0, limit: int = 10 ):
    
    query = db.query(Product).filter(Product.is_active == True)

    if name:
        query = query.filter(Product.name.ilike('%' + name + '%'))

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock is True:
        query = query.filter(Product.stock_quantity > 0)

    if sort_by == 'price':
        if order == 'asc':
            query = query.order_by(Product.price.asc())
        else:
            query = query.order_by(Product.price.desc())

    elif sort_by == 'created_at':
        if order == 'asc':
            query = query.order_by(Product.created_at.asc())
        else:
            query = query.order_by(Product.created_at.desc())

    else:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid sort field' )

    return query.offset(skip).limit(limit).all()


def get_product(product_id: int, db: Session):
    product = db.query(Product).filter( Product.id == product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    return product


def update_product( product_id: int, data: ProductUpdate, db: Session ):
    product = db.query(Product).filter( Product.id == product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    category = db.query(Category).filter( Category.id == data.category_id, Category.is_active == True ).first()

    if category is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    old_product = db.query(Product).filter( Product.sku == data.sku, Product.id != product_id ).first()

    if old_product is not None:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='SKU already exists' )

    product.name = data.name
    product.sku = data.sku
    product.description = data.description
    product.category_id = data.category_id
    product.price = data.price
    product.stock_quantity = data.stock_quantity

    try:
        db.commit()
        db.refresh(product)

        return product

    except IntegrityError:
        db.rollback()

        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='SKU already exists' )


def delete_product(product_id: int, db: Session):
    product = db.query(Product).filter( Product.id == product_id, Product.is_active == True ).first()

    if product is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Product not found' )

    product.is_active = False

    db.commit()

    return { 'message': 'Product deleted successfully' }