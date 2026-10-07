import os

from datetime import datetime
from datetime import timedelta

from dotenv import load_dotenv
from jose import jwt


load_dotenv()

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))


def create_token(user_id, role):
    expire_time = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)

    token_data = { 'sub': str(user_id), 'role': role, 'exp': expire_time }
    token = jwt.encode(token_data, secret_key, algorithm=algorithm)

    return token


def decode_token(token):
    token_data = jwt.decode(token, secret_key, algorithms=[algorithm])

    return token_data