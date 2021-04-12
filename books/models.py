# Set up database
from datetime import datetime
import urllib.parse as url_parse
from sqlalchemy import Table, Column, String, Integer, Text, MetaData, Date
from books.app import engine


meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('email', String, unique=True, nullable=False),
    Column('password', String, nullable=False)
)

books = Table(
    'books', meta,
    Column('id', Integer, primary_key=True),
    Column('isbn', String, nullable=False, unique=True),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('year', Date, nullable=False)
)

meta.create_all(engine)


class BookModel:
    def __init__(self, isbn: str, title: str, author: str, year: datetime):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def getPublicationYear(self):
        return self.year.utcnow()

    def getBookAmazonLink(self):
        return url_parse(f"https://www.amazon.com/s?k={self.title}&ref=nb_sb_noss")
