from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Telegram Username', [DataRequired()])
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        DataRequired(message="Can't be empty!"),
        Length(min=6)
    ])
    confirm_password = PasswordField(
        'Confirm Password', [EqualTo('password', message='passowrd must match!')])
    register_btn = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(
        message="Can't be empty!"), Length(min=6, max=35)])
    password = PasswordField('New Password', [
        DataRequired(message="Can't be empty!"),
        Length(min=6)
    ])
    remember_me = BooleanField('Remember me')
    login_btn = SubmitField('Sign In')


class BooksSearchForm(FlaskForm):
    search = StringField('')
