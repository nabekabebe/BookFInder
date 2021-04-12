import os

from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "769f213c4ea89e980132232fb84a528755cd1029110f2d274dfeabd6b404896a"
app.config["DATABASE_URL"] = "postgresql://postgres:niko1122@localhost/BookAPI"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
conn = engine.connect()
db = scoped_session(sessionmaker(bind=engine))
