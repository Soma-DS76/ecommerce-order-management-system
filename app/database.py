import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

database_url = os.getenv('DATABASE_URL')
engine = create_engine( database_url, echo=False )
session_local = sessionmaker( bind=engine, autocommit=False, autoflush=False )
base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()