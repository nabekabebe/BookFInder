from flask import jsonify, Blueprint, abort, request
from books.models import BookModel, book_schema, book_schemas
import json
from markupsafe import escape

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.route('/books', methods=['GET'])
def getBooks():
    from books.app import app
    from books.utils.db_helper import GetAll
    limit = request.args.get('limit')
    if(not limit):
        limit = 10

    query = "SELECT * FROM books LIMIT :limit"
    bQuery = GetAll(query, {'limit': escape(limit)})
    book_list = [BookModel.bookFactory(r[1:]) for r in bQuery]
    return book_schemas.dumps(book_list)


@api.route('/books/<int:book_id>', methods=['GET'])
def getBook(book_id=None):
    from books.app import app
    from books.utils.db_helper import GetOne

    if(not book_id):
        abort(500, description="The article you are looking for is not found!")

    book = GetOne('books', {'key': 'id', 'value': escape(book_id)})
    return book_schema.dumps(book)


@api.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


@api.errorhandler(500)
def page_not_found(e):
    return jsonify(error=str(e)), 500
