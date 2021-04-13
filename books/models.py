# Set up database
from datetime import datetime
from urllib.parse import quote, urlparse
from sqlalchemy import Table, Column, String, Integer, Text, MetaData, Date
from books.app import engine, conn


# meta = MetaData()

# users = Table(
#     'users', meta,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, nullable=False),
#     Column('email', String, unique=True, nullable=False),
#     Column('password', String, nullable=False)
# )

# books = Table(
#     'books', meta,
#     Column('id', Integer, primary_key=True),
#     Column('isbn', String, nullable=False, unique=True),
#     Column('title', String, nullable=False),
#     Column('author', String, nullable=False),
#     Column('year', Date, nullable=False)
# )

# meta.create_all(engine)


class BookModel:
    def __init__(self, isbn: str, title: str, author: str, year: datetime):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def getPublicationYear(self):
        return self.year.strftime('%Y')

    def getBookAmazonLink(self):
        print(
            urlparse(f"https://www.amazon.com/s?k={quote(self.title)}&ref=nb_sb_noss").geturl())
        return urlparse(f"https://www.amazon.com/s?k={quote(self.title)}&ref=nb_sb_noss").geturl()

    @staticmethod
    def bookFactory(book_info):
        book = BookModel(book_info[0], book_info[1],
                         book_info[2], book_info[3])
        return book
