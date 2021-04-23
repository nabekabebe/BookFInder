from sqlalchemy import text
from markupsafe import escape
from books.db import db
import requests

API_KEY = "AIzaSyCze2V2UZG7rmcpGOD6x1a1bAydFKluJOQ"
API_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:&key="


def InsertUser(values):
    q = text("""
    INSERT INTO users (username,email,password)
        VALUES (:username,:email,:password)
    """)
    id = db.execute(
        q, {'username': values['username'], 'email': values['email'], 'password': values['password']})
    db.commit()
    return id


def GetAll(stmt, values=None):
    q = text(stmt)
    data = db.execute(q, values).fetchall()
    db.commit()
    return data


def GetOne(db_name, values):
    q = text(f"""
    SELECT * FROM {db_name} WHERE {values['key']} = :h
    """)
    data = db.execute(q, {'h': values['value']}).fetchone()
    db.commit()
    return data


def DeleteOne(db_name, values):
    q = text(f"""
    DELETE FROM {db_name} WHERE {values['key']} = :h
    """)
    db.execute(q, {'h': values['value']})
    db.commit()


def getReviewByUserAndBook(userId, bookId):
    q = text(f"""
    SELECT * FROM reviews WHERE userId = :uid AND bookId = :bid
    """)
    data = db.execute(q, {'uid': userId, 'bid': bookId}).fetchone()
    return data


def InsertIntoReview(values):
    q = text("""
    INSERT INTO reviews (userId,bookId,comment,ratings, review)
        VALUES (:userId,:bookId,:comment,:ratings, :review)
    """)

    id = db.execute(
        q, {'userId': values['userId'], 'bookId': values['bookId'], 'ratings': values['ratings'], 'comment': values['comment'], 'review': values['review']})
    db.commit()
    return id


def InsertIntoBooks(values):
    q = text("""
    INSERT INTO books (id,isbn,title,author,year)
        VALUES (:id,:isbn,:title,:author,:year)
    """)

    id = db.execute(
        q, {'id': values['id'], 'isbn': values['isbn'], 'title': values['title'], 'author': values['author'], 'year': values['year']})
    db.commit()
    return id


def updateReviewLikeDislike(values, action):
    if(action > 0):
        q = text(f"""
        UPDATE reviews SET {values['key']} = {values['key']} + 1 WHERE id = :id 
        """)
    elif action < 0:
        q = text(f"""
        UPDATE reviews SET {values['key']} = {values['key']} - 1 WHERE id = :id
        """)
    else:
        q = text(f"""
        UPDATE reviews SET {values['key']} = {values['value']} WHERE id = :id 
        """)
    id = db.execute(q, {'id': values['id']})
    db.commit()
    return id


def getBookByIsbn(isbn):
    endpoint = "https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={key}".format(
        isbn=isbn, key=API_KEY)
    data = requests.get(endpoint).json()
    return data


def getBookByTitleOrAuthor(titleOrAuthor):
    endpoint = "https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&inauthor:{author}&key={key}".format(
        title=titleOrAuthor, author=titleOrAuthor, key=API_KEY)

    try:
        dataList = requests.get(endpoint).json()["items"]
    except Exception:
        dataList = []
    return dataList
