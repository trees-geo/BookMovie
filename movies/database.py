from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = "sqlite:///./movies.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={
    "check_same_thread": False
})
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()