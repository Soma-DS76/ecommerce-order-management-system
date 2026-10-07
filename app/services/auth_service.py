from fastapi import HTTPException
from fastapi import status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.cart import Cart
from app.schemas.auth import RegisterRequest
from app.utils.helpers import hash_password
from app.utils.helpers import verify_password
from app.auth.jwt import create_token


def create_user(data: RegisterRequest, db: Session):
    old_user = db.query(User).filter(User.email == data.email).first()

    if old_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    if data.role not in ['Admin', 'Customer']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid role')

    user = User(
        full_name=data.full_name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
        is_active=True,
    )

    try:
        db.add(user)
        db.flush()

        cart = Cart(customer_id=user.id)

        db.add(cart)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')


def login_user(data, db: Session):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    if verify_password(data.password, user.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    if user.is_active is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User account is inactive')

    access_token = create_token(user.id, user.role)

    return {'access_token': access_token, 'token_type': 'bearer'}
