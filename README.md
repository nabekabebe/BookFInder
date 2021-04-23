# Project 1: Books

This project is focused on providing books from different sources with their
reviews and ratings.

# Overview

This is a book review website. Users will be able to register for the website
and then log in using their email and password. Once they log in, they will be
able to search for books, leave reviews for individual books, and see the
reviews made by other people. Also a third-party API by Google Books is used to
pull in ratings from a google online book store. Finally, users will be able to
query for book details and book reviews the website’s API.

## Run the application:

1. Clone this repository into local machine.

2. In a terminal window, navigate into your project directory.

3. Run pip3 install -r requirements.txt in your terminal window to make sure
   that all of the necessary Python packages (Flask and SQLAlchemy, for
   instance) are installed.

4. Set the environment variable FLASK_APP to be <b>books<\b>. On a Mac or on
   Linux, the command to do this is export FLASK_APP=books. On Windows, the
   command is instead set FLASK_APP=books. You may optionally want to set the
   environment variable FLASK_DEBUG to 1, which will activate Flask’s debugger
   and will automatically reload the web application whenever you save a change
   to a file.

5. Set the environment variable DATABASE_URL (online database or local postgres
   database).

6. Before running the application separately run the import.py file in the
   project to setup the database tables (necessary!).

7. Run flask run to start up your Flask application by typing flask run on the
   terminal.

8. If you navigate to the URL provided by flask, you should see the text "Home
   page of the website"! ![alt text](./flask.png)

## Goodreads API

Goodreads is a popular book review website, and we’ll be using their API in this
project to get access to their review data for individual books.

1. Go to [https://www.goodreads.com/api] and sign up for a Goodreads account if
   you don’t already have one.

2. Navigate to [https://www.goodreads.com/api/keys] and apply for an API key.
   For “Application name” and “Company name” feel free to just write “project1,”
   and no need to include an application URL, callback URL, or support URL.
3. You should then see your API key. (For this project, we’ll care only about
   the “key”, not the “secret”.)
4. You can now use that API key to make requests to the Goodreads API,
   documented here. In particular, Python code like the below

```python
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
print(res.json())
```

where KEY is your API key, will give you the review and rating data for the book
with the provided ISBN number. In particular, you might see something like this
dictionary:

```json
{
  "books": [
    {
      "id": 29207858,
      "isbn": "1632168146",
      "isbn13": "9781632168146",
      "ratings_count": 0,
      "reviews_count": 1,
      "text_reviews_count": 0,
      "work_ratings_count": 26,
      "work_reviews_count": 113,
      "work_text_reviews_count": 10,
      "average_rating": "4.04"
    }
  ]
}
```

Note that work_ratings_count here is the number of ratings that this particular
book has received, and average_rating is the book’s average score out of 5.

# Requirements

Alright, it’s time to actually build your web application! Here are the
requirements:

1. **Registration**: Users should be able to register for your website,
   providing (at minimum) a username and password.

2. **Login**: Users, once registered, should be able to log in to your website
   with their username and password.

3. **Logout**: Logged in users should be able to log out of the site.

4. **Import**: Provided for you in this project is a file called books.csv,
   which is a spreadsheet in CSV format of 5000 different books. Each one has an
   ISBN number, a title, an author, and a publication year. In a Python file
   called import.py separate from your web application, write a program that
   will take the books and import them into your PostgreSQL database. You will
   first need to decide what table(s) to create, what columns those tables
   should have, and how they should relate to one another. Run this program by
   running python3 import.py to import the books into your database, and submit
   this program with the rest of your project code.

5. **Search**: Once a user has logged in, they should be taken to a page where
   they can search for a book. Users should be able to type in the ISBN number
   of a book, the title of a book, or the author of a book. After performing the
   search, your website should display a list of possible matching results, or
   some sort of message if there were no matches. If the user typed in only part
   of a title, ISBN, or author name, your search page should find matches for
   those as well!

6. **Book Page**: When users click on a book from the results of the search
   page, they should be taken to a book page, with details about the book: its
   title, author, publication year, ISBN number, and any reviews that users have
   left for the book on your website.

7. **Review Submission**: On the book page, users should be able to submit a
   review: consisting of a rating on a scale of 1 to 5, as well as a text
   component to the review where the user can write their opinion about a book.
   Users should not be able to submit multiple reviews for the same book.

8. **Goodreads Review Data**: On your book page, you should also display (if
   available) the average rating and number of ratings the work has received
   from Goodreads.

9. **API Access**: If users make a GET request to your website’s /api/<isbn>
   route, where <isbn> is an ISBN number, your website should return a JSON
   response containing the book’s title, author, publication date, ISBN number,
   review count, and average score. The resulting JSON should follow the format:

```json
{
  "title": "Memory",
  "author": "Doug Lloyd",
  "year": 2015,
  "isbn": "1632168146",
  "review_count": 28,
  "average_score": 5.0
}
```
