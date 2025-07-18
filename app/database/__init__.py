from os import getenv
from dotenv import load_dotenv
from pymysql import install_as_MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
install_as_MySQLdb()

engine = create_engine(getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


__all__ = [get_session, engine, Base]
