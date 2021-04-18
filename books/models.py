# Set up database
from datetime import datetime
from urllib.parse import quote, urlparse
from marshmallow import Schema
# from sqlalchemy import Table, Column, String, Integer, Text, MetaData, Date
# from books.app import engine, conn


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
    def __init__(self, isbn: str, title: str, author: str, year: datetime, id=None):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.total_rating = 0
        self.desc = ""
        self.avg_rating = 0
        self.image = ""
        self.language = "en"
        self.page_num = None

    def getPublicationYear(self):
        if self.year is datetime:
            return self.year.strftime('%Y')
        else:
            return self.year

    def getBookAmazonLink(self):
        print(
            urlparse(f"https://www.amazon.com/s?k={quote(self.title)}&ref=nb_sb_noss").geturl())
        return urlparse(f"https://www.amazon.com/s?k={quote(self.title)}&ref=nb_sb_noss").geturl()

    @staticmethod
    def bookFactory(book_info):
        book = BookModel(id=book_info[0], isbn=book_info[1],
                         title=book_info[2], author=book_info[3], year=book_info[4])
        return book

    @staticmethod
    def bookFromJSON(json_obj):
        book_list = []
        for book in json_obj:
            book_json = book.get("volumeInfo")
            if book_json:
                isbn = book_json.get("industryIdentifiers")[0].get(
                    "identifier") if book_json.get("industryIdentifiers") else None
                title = book_json.get("title")
                author = book_json.get("authors")[0]
                year = book_json.get("publishedDate")
                book_model = BookModel(isbn=isbn, title=title,
                                       author=author, year=year)
                try:
                    book_model.desc = book_json.get("description")
                    book_model.avg_rating = book_json.get("averageRating")
                    book_model.total_rating = book_json.get("ratingsCount")
                    book_model.language = book_json.get("language")
                    book_model.page_num = book_json.get("pageCount")
                    book_model.image = book_json.get("imageLinks").get(
                        "thumbnail") if book_json.get("imageLinks") else None
                except Exception as e:
                    pass
                book_list.append(book_model)
        return book_list


class BookSchema(Schema):
    """ Book dict serializer """
    class Meta:
        # fields to serialize
        fields = ('id', 'isbn', 'title', 'author', 'year')


book_schema = BookSchema()
book_schemas = BookSchema(many=True)
