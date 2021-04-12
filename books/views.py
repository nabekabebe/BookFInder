from flask import render_template, url_for, redirect, flash, request, session, abort, current_app, g
from markupsafe import escape

from books.app import app, conn, db
from books.models import users
from books.forms import RegistrationForm, LoginForm


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            s = db()
            ins = users.insert().values(username=str(form.username.data),
                                        email=form.email.data, password=form.password.data)
            result = conn.execute(ins)
            s = users.select()
            result2 = conn.execute(s)
            for row in result2:
                print(row)
            print(result.inserted_primary_key)
            flash(f'user {form.username.data} created successfully!', 'success')
            redirect(url_for('login'))
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
            user_query = users.select().where(users.c.email == form.email.data)
            user = conn.execute(user_query).fetchone()
            if(user and user.password == form.password.data):
                session['user_id'] = user.id
                g.user = user
                return redirect(url_for('home'))
            else:
                flash("Login Failed! bad credentials.0,", 'danger')
                return redirect(url_for('login'))
        print("form error")
        return "Invalid Form!"
    else:
        return render_template('auth/login.html', title="Login", form=form)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('user_id', None)
    g.user = None
    return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template("index.html", title="home page")


@app.route('/home')
def home():
    if 'user_id' in session:
        print("session exists!")
        if(not g.get('user')):
            print('user doesnt exits')
            user_query = users.select().where(users.c.id == session['user_id'])
            g.user = conn.execute(user_query).fetchone()
            print(g.user.username)
        return render_template('home.html', title="index")
    return render_template('index.html', title="Home")
