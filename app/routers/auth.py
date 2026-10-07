from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse
from app.schemas.auth import UserResponse
from app.services.auth_service import create_user
from app.services.auth_service import login_user
from app.auth.dependencies import get_current_user
from app.auth.dependencies import get_admin_user


router = APIRouter()


@router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED )
def register( data: RegisterRequest, db: Session = Depends(get_db),
              current_user: User = Depends(get_admin_user)):
    return create_user(data, db)


@router.post( '/login', response_model=TokenResponse )
def login( data: LoginRequest, db: Session = Depends(get_db) ):
    return login_user(data, db)


@router.get( '/me', response_model=UserResponse )
def get_me( current_user: User = Depends(get_current_user) ):
    return current_user