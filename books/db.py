import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
conn = engine.connect()
db = scoped_session(sessionmaker(bind=engine))
