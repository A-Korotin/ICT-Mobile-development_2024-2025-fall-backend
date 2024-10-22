from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
engine = create_engine(CONNECTION_STRING)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
