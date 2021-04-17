from sqlalchemy import text
from flask import current_app, g
from markupsafe import escape
from .db import get_db


def InsertUser(values):
    db = get_db()
    q = text("""
    INSERT INTO users (username,email,password)
        VALUES (:username,:email,:password)
    """)
    id = db.execute(
        q, {'username': values['username'], 'email': values['email'], 'password': values['password']})
    print(id.lastrowid)


def GetAll(stmt, values):
    db = get_db()
    q = text(stmt)
    return db.execute(q, values).fetchall()


def GetOne(db_name, values):
    db = get_db()
    q = text(f"""
    SELECT * FROM {db_name} WHERE {values['key']} = :holder 
    """)
    return db.execute(q, {'holder': values['value']}).fetchone()
