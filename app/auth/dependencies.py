from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.jwt import decode_token
from app.models.user import User


security = HTTPBearer(auto_error=False)


def get_current_user( credentials: HTTPAuthorizationCredentials = Depends(security),
                      db: Session = Depends(get_db) ):
    if credentials is None:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication required' )

    token = credentials.credentials

    try:
        token_data = decode_token(token)
        user_id = token_data.get('sub')

        if user_id is None:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

        if user.is_active is False:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail='User account is inactive')

        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid or expired token' )


def get_admin_user( current_user: User = Depends(get_current_user) ):
    if current_user.role != 'Admin':
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail='Admin access required' )

    return current_user


def get_customer_user( current_user: User = Depends(get_current_user) ):
    if current_user.role != 'Customer':
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN,detail='Customer access required' )

    return current_user