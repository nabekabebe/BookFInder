# Set up database
from datetime import datetime
from urllib.parse import quote, urlparse
from marshmallow import Schema
from books.utils.db_helper import GetOne
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
        if isinstance(self.year, str):
            return self.year
        elif self.year is None:
            return "Unkown"
        else:
            return self.year.year

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
                author = book_json.get("authors")[0] if book_json.get(
                    "authors") else "unkown"
                year = datetime(int(book_json.get("publishedDate")), 1, 1) if len(
                    book_json.get("publishedDate").strip()) == 4 else book_json.get("publishedDate")
                book_model = BookModel(isbn=isbn, title=title,
                                       author=author, year=year)
                try:
                    book_model.desc = book_json.get("description")
                    book_model.avg_rating = book_json.get("averageRating")
                    book_model.total_rating = int(
                        book_json.get("ratingsCount"))
                    book_model.language = book_json.get("language")
                    book_model.page_num = book_json.get("pageCount")
                    book_model.image = book_json.get("imageLinks").get(
                        "thumbnail") if book_json.get("imageLinks") else None
                except Exception as e:
                    pass
                book_list.append(book_model)
        return book_list


class ReviewModel:
    def __init__(self, id, userId, bookId, comment, ratings, review, date):
        self.id = id
        self.userId = userId
        self.bookId = bookId
        self.review = review
        self.comment = comment
        self.ratings = ratings
        self.date = date

    @staticmethod
    def reviewFromTuple(reviewList):
        reviews = []
        for rev in reviewList:
            revObj = ReviewModel(rev[0], rev[1], rev[2],
                                 rev[3], rev[4], rev[5], rev[8])
            revObj.name = GetOne('users', {'key': 'id',
                                           'value': int(rev[1])})[1]
            reviews.append(revObj)
        return reviews

    # def __repr__(self):
    #     print(
    #         f"Review(id:{self.id}, userId:{self.userId}, bookId:{self.bookId}, ratings:{self.ratings}")


class BookSchema(Schema):
    """ Book dict serializer """
    class Meta:
        # fields to serialize
        fields = ('id', 'isbn', 'title', 'author', 'year')


class ReviewSchema(Schema):
    """ Book dict serializer """
    class Meta:
        # fields to serialize
        fields = ('id', 'userid', 'bookid', 'comment',
                  'ratings', 'review', 'date')


book_schema = BookSchema()
book_schemas = BookSchema(many=True)

review_schema = ReviewSchema()
review_schemas = ReviewSchema(many=True)
