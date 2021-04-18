from datetime import datetime
import functools

from flask import Blueprint, render_template, url_for, redirect, flash, request, session, abort, g, jsonify
from markupsafe import escape

from books.models import BookModel
from books.forms import RegistrationForm, LoginForm, BooksSearchForm
from books.utils.db_helper import InsertUser, GetOne, GetAll, getBookByIsbn, getBookByTitleOrAuthor
from sqlalchemy import text

view_bp = Blueprint('app', __name__, url_prefix='/')

"""
Pre Auth middlewares
"""


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("login required!", 'danger')
            return redirect(url_for('app.login'))
        return view(**kwargs)
    return wrapped_view


def not_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for('app.home'))
        return view(**kwargs)
    return wrapped_view


@view_bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        print("user session doesnt exits!")
        g.user = None
    else:
        g.user = GetOne('users', {'key': 'id', 'value': user_id})


"""
Webpage views
"""


@view_bp.route("/")
@not_login_required
def index():
    return render_template("index.html", title="home page")


@view_bp.route('/home', methods=('GET', 'POST'))
@login_required
def home():
    searchForm = BooksSearchForm(request.form)
    query = "SELECT * FROM books LIMIT :limit"
    bQuery = GetAll(query, {'limit': 10})
    if request.method == 'POST' and searchForm.search.data:
        sq = escape(searchForm.search.data)
        query = f"SELECT * FROM books WHERE (title ILIKE :title OR isbn ILIKE :isbn OR author ILIKE :author) {'LIMIT :limit' if False else ''}"
        isNum = '%'+sq+'%' if sq.isdigit() else '-1'
        sq = '%'+sq+'%'
        bQuery = GetAll(
            query, {'limit': 10, 'title': sq, 'isbn': isNum, 'author': sq})
        if len(bQuery) == 0:
            bQuery = getBookByTitleOrAuthor(sq)
            books_list_fromJson = BookModel.bookFromJSON(bQuery)
            return render_template('home.html', title="index", book_list=books_list_fromJson, searchForm=searchForm)
    book_list = [BookModel.bookFactory(r) for r in bQuery]
    return render_template('home.html', title="index", book_list=book_list, searchForm=searchForm)


@view_bp.route('/book/<bookId>')
def bookDetail(bookId):
    if bookId.isdigit() and int(bookId) < 8000:
        book = GetOne('books', {'key': 'id', 'value': int(bookId)})
        model = BookModel.bookFactory(book)
    else:
        book = GetOne('books', {'key': 'isbn', 'value': bookId})
    if book is None:
        book_info = getBookByIsbn(bookId)
        model = BookModel.bookFromJSON([book_info["items"][0]])[0]
    else:
        model = BookModel.bookFactory(book)
        try:
            book_json = book_info.get("items")[0].get("volumeInfo")
            if book_json:
                model.desc = book_json.get("description")
                model.avg_rating = book_json.get("averageRating")
                model.total_rating = book_json.get("ratingsCount")
                model.language = book_json.get("language")
                model.page_num = book_json.get("pageCount")
                model.image = book_json.get("imageLinks").get(
                    "thumbnail") if book_json.get("imageLinks") else None
        except Exception as e:
            pass
    return render_template('book_detail.html', book=model, title=model.title)


@view_bp.route('/me/<int:id>', methods=('GET', 'POST'))
@login_required
def getMe(id):
    user = GetOne('users', {'key': 'id', 'value': id})
    print("this: ", user)
    if(user):
        return jsonify(list(user))
    else:
        return jsonify({"status": 404, "message": "No user with that id"})


@view_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""
Authentication views
"""


@view_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = GetOne('users', {'key': 'email', 'value': form.email.data})
            if user and form.email.data == user[2]:
                flash(f'User with this email already exists!', 'danger')
                return redirect(url_for('app.register'))
            values = {'username': form.username.data,
                      'email': form.email.data, 'password': form.password.data}
            InsertUser(values)
            return redirect(url_for('app.login'))
        else:
            print("form error")
            flash(f'Error creating user!', 'danger')
            print(form)
            return redirect(url_for('app.register'))
    return render_template('auth/register.html', title="Register", form=form)


@view_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            user = GetOne('users', {'key': 'email', 'value': form.email.data})
            if(user and user.password == form.password.data):
                session['user_id'] = user[0]
                g.user = user
                return redirect(url_for('app.home'))
            else:
                flash("Login Failed! bad credentials.0,", 'danger')
                return redirect(url_for('app.login'))
            pass
        else:
            print("form error")
            return "Invalid Form!"
    else:
        return render_template('auth/login.html', title="Login", form=form)


@view_bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('user_id', None)
    g.user = None
    return redirect(url_for('app.index'))
