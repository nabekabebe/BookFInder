import csv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime as dtime
import sys
from .config import DATABASE_URL


def rundb():
    main()


def main():
    db_path = DATABASE_URL
    if len(sys.argv) >= 2 and sys.argv[1]:
        # accept database path
        db_path = sys.argv[1]
    else:
        raise RuntimeError(
            "DATABASE type is not specified in the command arguments! set DATABASE_TYPE to LOCAL or REMOTE")

    engine = create_engine(
        db_path, isolation_level="READ UNCOMMITTED")
    con = engine.connect()
    db = scoped_session(sessionmaker(bind=engine))

    schema_path = '../schema.sql'
    if len(sys.argv) >= 3 and sys.argv[2]:
        # accept sql schema path
        schema_path = sys.argv[2]
    try:
        f = open(schema_path, 'r')
        db.execute(text(f.read()))
        db.commit()
        print("schema created!")
    except StatementError as error:
        print(error.orig)
    except Exception as e:
        print("Error creating db: ", e)

    books_path = '../books.csv'
    if len(sys.argv) >= 4 and sys.argv[3]:
        # accept books csv data path
        books_path = sys.argv[3]

    with open(books_path, 'rt') as csv_file:
        csv_reader = csv.DictReader(csv_file).reader
        query_raw = text(
            "INSERT INTO books(isbn, title, author, year) VALUES(:isbn,:title,:author,:year)")
        result = db.execute(query_raw,
                            [{'isbn': row[0], 'title':row[1], 'author':row[2], 'year':dtime(int(row[3]), 1, 1)}
                             for index, row in enumerate(csv_reader) if index > 0]
                            )
        db.commit()
        print("books inserted!")


if __name__ == '__main__':
    main()
