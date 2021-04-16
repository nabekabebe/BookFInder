from datetime import datetime
import functools

from flask import render_template, url_for, redirect, flash, request, session, abort, current_app, g
from markupsafe import escape
from flask import jsonify

from books.app import app
from books.models import BookModel
from books.forms import RegistrationForm, LoginForm, BooksSearchForm
from books.utils.db_helper import InsertUser, GetOne, GetAll


"""
Pre Auth middlewares
"""


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("login required!", 'danger')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


@app.before_request
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


@app.route("/")
def index():
    return render_template("index.html", title="home page")


@app.route('/home', methods=('GET', 'POST'))
@login_required
def home():
    searchForm = BooksSearchForm(request.form)
    query = "SELECT * FROM books LIMIT :limit"
    bQuery = GetAll(query, {'limit': 10})
    book_list = [BookModel.bookFactory(r[1:]) for r in bQuery]
    if request.method == 'POST' and searchForm.search.data:
        sq = searchForm.search.data
        query = "SELECT * FROM books WHERE isbn LIKE %:isbn OR title LIKE %:title LIMIT :limit"
        bQuery = GetAll(query, {'limit': 10, 'isbn': sq, 'title': sq})

    book_list = [BookModel.bookFactory(r[1:]) for r in bQuery]
    return render_template('home.html', title="index", book_list=book_list, searchForm=searchForm)


@app.route('/me/<int:id>', methods=('GET', 'POST'))
@login_required
def getMe(id):
    user = GetOne('users', {'key': 'id', 'value': id})
    print("this: ", user)
    if(user):
        return jsonify(list(user))
    else:
        return jsonify({"status": 404, "message": "No user with that id"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""
Authentication views
"""


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = GetOne('users', {'key': 'email', 'value': form.email.data})
            if user and form.email.data == user[2]:
                flash(f'User with this email already exists!', 'danger')
                return redirect(url_for('register'))
            values = {'username': form.username.data,
                      'email': form.email.data, 'password': form.password.data}
            InsertUser(values)
            return redirect(url_for('login'))
        else:
            print("form error")
            flash(f'Error creating user!', 'danger')
            print(form)
            return redirect(url_for('register'))
    return render_template('auth/register.html', title="Register", form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            user = GetOne('users', {'key': 'email', 'value': form.email.data})
            if(user and user.password == form.password.data):
                session['user_id'] = user[0]
                g.user = user
                return redirect(url_for('home'))
            else:
                flash("Login Failed! bad credentials.0,", 'danger')
                return redirect(url_for('login'))
            pass
        else:
            print("form error")
            return "Invalid Form!"
    else:
        return render_template('auth/login.html', title="Login", form=form)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('user_id', None)
    g.user = None
    return redirect(url_for('index'))
