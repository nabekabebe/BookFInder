from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
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
    remember_me = BooleanField('Remember me', default=False)
    login_btn = SubmitField('Sign In')


class BooksSearchForm(FlaskForm):
    search = StringField('')


class BookReview(FlaskForm):
    options = [(0, 'Choose Rating'), (1, 'One⭐'), (2, 'Two⭐'),
               (3, 'Three⭐'), (4, 'Four⭐'), (5, 'Five⭐')]
    # sort_options = ["recent", "likes"]
    comment = StringField("Comment", [DataRequired()])
    review = TextAreaField("Write Review", [DataRequired()])
    ratings = SelectField("Choose rating", choices=options)
    # sort = SelectField("Sort By", choices=sort_options)
    submit = SubmitField("submit")
