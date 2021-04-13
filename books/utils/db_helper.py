from sqlalchemy import text
from books.app import conn


def InserIntoUsers(values):
    q = text("""
    INSERT INTO users (username,email,password)
        VALUES (:username,:email,:password)
    """)
    with conn.begin():
        id = conn.execute(
            q, username=values['username'], email=values['email'], password=values['password'])
        print(id.lastrowid)
