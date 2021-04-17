from sqlalchemy import text
from markupsafe import escape
from books.db import db


def InsertUser(values):
    q = text("""
    INSERT INTO users (username,email,password)
        VALUES (:username,:email,:password)
    """)
    id = db.execute(
        q, {'username': values['username'], 'email': values['email'], 'password': values['password']})
    print(id.lastrowid)


def GetAll(stmt, values=None):
    q = text(stmt)
    return db.execute(q, values).fetchall()


def GetOne(db_name, values):
    q = text(f"""
    SELECT * FROM {db_name} WHERE {values['key']} = :holder 
    """)
    return db.execute(q, {'holder': values['value']}).fetchone()
