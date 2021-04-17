from flask import jsonify, Blueprint, abort, request
from books.models import BookModel, book_schema, book_schemas
from markupsafe import escape
from .utils.db_helper import GetAll, GetOne
api = Blueprint('api', __name__, url_prefix='/api/v1')

API = Api(api)


@API.route('/books', methods=['GET'])
class AllBooks(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        limit = request.args.get('limit')
        if(not limit):
            limit = 10
        query = "SELECT * FROM books LIMIT :limit"
        bQuery = GetAll(query, {'limit': escape(limit)})
        book_list = [book_schema.dumps(
            BookModel.bookFactory(r[1:])) for r in bQuery]
        return book_schemas.dumps(book_list)


@API.route('/books/<int:book_id>', methods=['GET'])
class Book(Resource):
    def get(self, book_id):
        if(1 == book_id):
            API.abort(
                code=400, message="Sorry. I'm afraid I can't do that.")
            # abort(500, description="The article you are looking for is not found!")
        book = GetOne('books', {'key': 'id', 'value': escape(book_id)})
        return book_schema.dumps(book)


@api.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


@api.errorhandler(500)
def page_not_found(e):
    return jsonify(error=str(e)), 500
