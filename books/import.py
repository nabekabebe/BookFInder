import csv
from sqlalchemy import create_engine, text
from datetime import datetime as dtime
import sys

engine = create_engine("postgresql://postgres:niko1122@localhost/BookAPI")
con = engine.connect()

books_path = '../books.csv'
if sys.argv[1]:
    books_path = sys.argv[1]

with open(books_path, 'rt') as csv_file:
    csv_reader = csv.DictReader(csv_file).reader
    query_raw = text(
        "INSERT INTO books(isbn, title, author, year) VALUES(:isbn,:title,:author,:year)")
    result = con.execute(query_raw,
                         [{'isbn': row[0], 'title':row[1], 'author':row[2], 'year':dtime(int(row[3]), 1, 1)}
                             for index, row in enumerate(csv_reader) if index > 0]
                         )
