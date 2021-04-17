import csv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import StatementError
from datetime import datetime as dtime
import sys
import os


def rundb():
    main()


def main():
    db_path = "postgresql://postgres:niko1122@localhost/Test"
    if len(sys.argv) >= 2 and sys.argv[1]:
        db_path = sys.argv[1]
    else:
        raise RuntimeError(
            "DATABASE_URL is not specified in the command arguments!")

    engine = create_engine(db_path)
    con = engine.connect()

    schema_path = '/home/niko/Documents/code/3rd yr/flask/project_01_book_api/projectone-nabekabebe/schema.sql'
    if len(sys.argv) >= 3 and sys.argv[2]:
        schema_path = sys.argv[2]
    try:
        f = open(schema_path, 'r')
        con.execute(f.read())
        print("schema created!")
    except StatementError as error:
        print(error.orig)
    except Exception as e:
        print("Error creating db: ", e)

    books_path = '../books.csv'
    if len(sys.argv) >= 4 and sys.argv[3]:
        books_path = sys.argv[3]

    with open(books_path, 'rt') as csv_file:
        csv_reader = csv.DictReader(csv_file).reader
        query_raw = text(
            "INSERT INTO books(isbn, title, author, year) VALUES(:isbn,:title,:author,:year)")
        result = con.execute(query_raw,
                             [{'isbn': row[0], 'title':row[1], 'author':row[2], 'year':dtime(int(row[3]), 1, 1)}
                              for index, row in enumerate(csv_reader) if index > 0]
                             )
        print("books inserted!")


if __name__ == '__main__':
    main()
