from dotenv import load_dotenv
import os
from sqlmodel import create_engine
from sqlmodel import SQLModel, Session
from .logger import logger
from sqlalchemy.exc import OperationalError

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))


def create_table():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Table created successfully")
    except Exception as e:
        logger.error(e)
        return None


def get_session():
    try:
        with Session(engine) as session:
            yield session
            logger.info("Database connection succesfull")
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return None
