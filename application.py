import os

from flask import Flask, session, render_template, url_for, redirect, flash, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "769f213c4ea89e980132232fb84a528755cd1029110f2d274dfeabd6b404896a"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html", title="home page")


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("nice")
        flash(f'user {form.username.data} created successfully!', 'success')
        redirect(url_for('index'))
    else:
        print("form error")
        flash(f'Error creating user!', 'danger')
        print(form)
    return render_template('auth/register.html', title="Register", form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate():
        print("nice")
    else:
        print("form error")
    return render_template('auth/login.html', title="Login", form=form)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    return redirect(url_for('index'))
