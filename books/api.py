from flask import jsonify, Blueprint, abort, request
from books.models import BookModel, book_schema, book_schemas
from markupsafe import escape
from books.utils.db_helper import GetAll, GetOne, getBookByIsbn
from books.init_api import API
from flask_restplus import Resource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@API.route('/books', methods=['GET'])
class AllBooks(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        limit = request.args.get('limit')
        if(not limit):
            limit = 10
        query = "SELECT * FROM books LIMIT :limit"
        bQuery = GetAll(query, {'limit': escape(limit)})
        print(bQuery)
        book_list = [BookModel.bookFactory(r[1:]) for r in bQuery]
        return book_schemas.dump(book_list)


@API.route('/books/<int:book_id>', methods=['GET'])
class Book(Resource):
    def get(self, book_id):
        if book_id is None:
            API.abort(
                code=400, message="Invalid request!")
        book = GetOne('books', {'key': 'id', 'value': escape(book_id)})
        if book is None:
            API.abort(
                code=400, message="Sorry, coudn't find the book!")
            # abort(500, description="The article you are looking for is not found!")
        return book_schema.dumps(book)


@API.route('/books/isbn/<isbn>', methods=['GET'])
class Book(Resource):
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


@ api_bp.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


@ api_bp.errorhandler(500)
def page_not_found(e):
    return jsonify(error=str(e)), 500
