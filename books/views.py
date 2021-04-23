from datetime import datetime
import functools

from flask import Blueprint, render_template, url_for, redirect, flash, request, session, abort, g, jsonify
from markupsafe import escape

from books.models import BookModel, ReviewModel
from books.forms import RegistrationForm, LoginForm, BooksSearchForm, BookReview
from books.utils.db_helper import db, InsertUser, GetOne, GetAll, getBookByIsbn, getBookByTitleOrAuthor, getReviewByUserAndBook, InsertIntoReview, InsertIntoBooks, DeleteOne
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
        g.user = GetOne('users', {'key': 'id', 'value': int(user_id)})


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
            print("Search online api")
            bQuery = getBookByTitleOrAuthor(sq)
            books_list_fromJson = BookModel.bookFromJSON(bQuery)
            return render_template('home.html', title="index", book_list=books_list_fromJson, searchForm=searchForm)
    book_list = [BookModel.bookFactory(r) for r in bQuery]
    return render_template('home.html', title="index", book_list=book_list, searchForm=searchForm)


@view_bp.route('/book/<bookId>')
def bookDetail(bookId):
    reviewForm = BookReview()
    if bookId.isdigit() and int(bookId) < 8000:
        book = GetOne('books', {'key': 'id', 'value': int(bookId)})
        print("Searching from local database")
    else:
        book = GetOne('books', {'key': 'isbn', 'value': bookId})
        print("Searching from local database")
    if book is None:
        print("Searching on the internet")
        book_info = getBookByIsbn(bookId)
        book_list = book_info.get(
            "items")[0] if book_info.get("items") else None
        if book_list is not None:
            model = BookModel.bookFromJSON([book_list])[0]
            values = {'id': model.isbn if model.isbn else bookId, 'isbn': model.isbn if model.isbn else bookId,
                      'title': model.title if model.title else "Unkown", 'author': model.author if model.author else "Unkown", 'year': model.year}
            InsertIntoBooks(values)
            print("Trump isbn: ", model.isbn)
        else:
            return render_template('404.html'), 404
    else:
        model = BookModel.bookFactory(book)
        try:
            book_json = getBookByIsbn(book.isbn).get(
                "items")[0] if getBookByIsbn(book.isbn).get("items") else None
            book_volume = book_json.get(
                "volumeInfo") if book_json else None
            if book_volume:
                model.desc = book_volume.get("description")
                model.avg_rating = int(book_volume.get("averageRating"))
                model.total_rating = book_volume.get("ratingsCount")
                model.language = book_volume.get("language")
                model.page_num = book_volume.get("pageCount")
                model.image = book_volume.get("imageLinks").get(
                    "thumbnail") if book_volume.get("imageLinks") else None

        except Exception as e:
            print("crashed", e)
            pass
    reviews = ReviewModel.reviewFromTuple(
        GetAll(f"SELECT * FROM reviews WHERE bookId = {bookId} ORDER BY id DESC"))
    myTotalRating = 0
    if len(reviews) > 0:
        myTotalRating = (functools.reduce(
            lambda x, y: x+y, [r.ratings for r in reviews])) / len(reviews)
    return render_template('book_detail.html', book=model, title=model.title, reviewForm=reviewForm, reviews=reviews, totalRating=myTotalRating)


@view_bp.route('/book/<int:id>/review', methods=['GET', 'POST'])
def review(id=None):
    reviewForm = BookReview(request.form)
    if request.method == "POST":
        # save book review
        if reviewForm.validate_on_submit():
            comment = reviewForm.comment.data
            review = reviewForm.review.data
            ratings = reviewForm.ratings.data
            if ratings == 0:
                flash("Please choose rating", "warning")
                return redirect(url_for('app.bookDetail', bookId=id))

            # add review to database | check if this user has submited review before
            userId = session['user_id']
            data = getReviewByUserAndBook(userId, id)
            if data:
                flash("You have already submitted review", "warning")
                return redirect(url_for('app.bookDetail', bookId=id))

            values = {'userId': userId, 'bookId': id,
                      'ratings': ratings, 'comment': comment, 'review': review}
            row_id = InsertIntoReview(values)
            if not row_id:
                flash("Unable to add review!", "danger")
                return redirect(url_for('app.bookDetail', bookId=id))
            flash("Review added successfully!", "success")
            return redirect(url_for('app.bookDetail', bookId=id))
        else:
            flash("Error on submitting review", "danger")
            return redirect(url_for('app.bookDetail', bookId=id))
    elif request.method == "GET":
        # return book review
        return redirect(url_for('app.bookDetail', bookId=id))


@view_bp.route('/book/<int:reviewId>/review/<int:userId>')
@login_required
def review_delete(reviewId, userId):
    review = GetOne('reviews', {'key': 'id', 'value': reviewId})
    print(review, reviewId, userId)
    if not review:
        flash("There is no review with this id", "danger")
        return redirect(url_for('app.home'))
    bookId = review[2]
    DeleteOne('reviews', {'key': 'id', 'value': reviewId})
    flash("Review deleted successfully!", "success")
    return redirect(url_for('app.bookDetail', bookId=bookId))


@view_bp.route('/me/<int:id>', methods=('GET', 'POST'))
@login_required
def getMe(id):
    user = GetOne('users', {'key': 'id', 'value': int(id)})
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
            user = GetOne('users', {'key': 'email',
                          'value': form.email.data.lower()})
            if user and (form.email.data).lower() == user[2]:
                flash(f'User with this email already exists!', 'danger')
                return redirect(url_for('app.register'))
            values = {'username': form.username.data,
                      'email': form.email.data.lower(), 'password': form.password.data}
            InsertUser(values)

            flash("Registration successful!", "success")
            return redirect(url_for('app.login'))
        else:
            print("form error")
            flash(f'Error creating user!', 'danger')
            print(form)
            return redirect(url_for('app.register'))
    return render_template('auth/register.html', title="Register", form=form)


@ view_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            rememberMe = form.remember_me.data
            user = GetOne('users', {'key': 'email',
                          'value': form.email.data.lower()})
            if(user and user.password == form.password.data):
                print("Remember: ", rememberMe)
                if rememberMe:
                    print("Session made permanent")
                    session.permanent = True
                else:
                    session.permanent = False
                session['user_id'] = user[0]
                g.user = user
                return redirect(url_for('app.home'))
            else:
                flash("Login Failed! bad credentials.", 'danger')
                return redirect(url_for('app.login'))
        else:
            flash("Please fill all required inputs.", 'danger')
            return redirect(url_for('app.login'))
    else:
        return render_template('auth/login.html', title="Login", form=form)


@ view_bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('user_id', None)
    g.user = None
    return redirect(url_for('app.index'))
