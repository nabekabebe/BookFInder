import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"),
                       echo=True, pool_size=20, max_overflow=0)
conn = engine.connect()
db = scoped_session(sessionmaker(bind=engine))
