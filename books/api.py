from flask import jsonify, Blueprint, abort, request
from books.models import BookModel, book_schema, book_schemas, ReviewModel, review_schema, review_schemas
from markupsafe import escape
from books.utils.db_helper import GetAll, GetOne, getBookByIsbn
from books.init_api import API
from flask_restplus import Resource, Namespace

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

api_books = Namespace(
    "Books", description="Get list of availabe books by id and isbn")
api_reviews = Namespace("Reviews", description="Get reviews for books by id")

API.add_namespace(api_books)
API.add_namespace(api_reviews)


@api_books.route('/books', methods=['GET'])
class AllBooks(Resource):  # Create a RESTful resource
    @API.doc(params={'limit': {'description': 'limit the number of books returned',
                               'type': 'int', 'default': 10}})
    def get(self):  # Create GET endpoint
        limit = request.args.get('limit')
        if(not limit):
            limit = 10
        query = "SELECT * FROM books LIMIT :limit"
        bQuery = GetAll(query, {'limit': escape(limit)})
        print(bQuery)
        book_list = [BookModel.bookFactory(r) for r in bQuery]
        return book_schemas.dump(book_list)


@api_books.route('/books/<int:book_id>', methods=['GET'])
class BookById(Resource):
    def get(self, book_id):
        if book_id is None:
            API.abort(
                code=400, message="Invalid request!")
        book = GetOne('books', {'key': 'id', 'value': escape(book_id)})
        if book is None:
            API.abort(
                code=400, message="Sorry, coudn't find the book!")
            # abort(500, description="The article you are looking for is not found!")
        return book_schema.dump(book)


@api_books.route('/books/isbn/<isbn>', methods=['GET'])
class BookByISBN(Resource):
    def get(self, isbn):
        if isbn is None:
            API.abort(
                code=400, message="Please provide isbn number!")
        data = getBookByIsbn(isbn)
        if data is None:
            API.abort(
                code=400, message="Sorry, coudn't find the book!")
            # abort(500, description="The article you are looking for is not found!")
        return data


@api_reviews.route('/books/<int:book_id>/reviews/', methods=['GET'])
class ReviewByBookId(Resource):
    def get(self, book_id):
        if book_id is None:
            API.abort(
                code=400, message="Invalid request!")
        reviews = ReviewModel.reviewFromTuple(
            GetAll(f"SELECT * FROM reviews WHERE bookid = {book_id} ORDER BY id DESC"))
        print(reviews)
        if reviews is None:
            API.abort(
                code=400, message="Sorry, coudn't find the book!")
            # abort(500, description="The article you are looking for is not found!")
        return review_schemas.dump(reviews)


@ api_bp.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


@ api_bp.errorhandler(500)
def page_not_found(e):
    return jsonify(error=str(e)), 500
