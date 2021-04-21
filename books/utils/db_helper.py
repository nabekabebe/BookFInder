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
    db.close()
    return id


def GetAll(stmt, values=None):
    q = text(stmt)
    data = db.execute(q, values).fetchall()
    db.close()
    return data


def GetOne(db_name, values):
    q = text(f"""
    SELECT * FROM {db_name} WHERE {values['key']} = :holder 
    """)
    data = db.execute(q, {'holder': values['value']}).fetchone()
    db.close()
    return data


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
