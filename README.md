# Project 1: Books by Nabek Abebe

This project is focused on providing books from different sources with their
reviews and ratings.

# Overview

This is a book review website. Users will be able to register for the website
and then log in using their email and password. Once they log in, they will be
able to search for books, leave reviews for individual books, and see the
reviews made by other people. Also a third-party API by Google Books is used to
pull in ratings from a google online book store. Finally, users will be able to
query for book details and book reviews the website’s API.

# Features

1. The website fetches books from local database with more than 5000 books pre
   populated.
2. Users can search for books by book ISBN, title and author.
3. If book are not found on the local database the website will query the Google
   Books API and display the books.
4. For every book queried the website will perform additional api query to
   populate the response with reach book details like total google books rating
   and local user ratings and reviews, book cover image, publication year,
   authors, book descriptions and so on.
5. The website will provide Amazon link to purchase the books listed.
6. Users can put their own reviews and rating which will get merged with the
   review and rating provided by other site users and also ratings from the
   google API contributing to the overall ratings and number of book's review.
7. Users cannot add multiple reviews for the same book although they can delete
   their own review and add another.
8. The Website provides convinient way to get books and reviews from dedicated
   api. The api method supported is only the http "GET" method.

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
   project to setup the database tables (necessary!). (provide database URL from
   the terminal to the enviroment!)

7. Run flask run to start up your Flask application by typing flask run on the
   terminal.

8. If you navigate to the URL provided by flask, you should see the text "Home
   page of the website"! ![alt text](./flask.png)

=> Heroku Database URl =
postgresql://jjjwivytsimjwi:e2bdcc0bd14397dcb667d49cebf96b9fb480f48ee8b4c16f051a52182c16effa@ec2-18-233-83-165.compute-1.amazonaws.com:5432/dc02n7i8oqjtit

## API Usage

The website provides API access to query books and review using nicely formatted
Swagger UI. The api doesn't require and authentication or developer keys.

Navigate To: http://127.0.0.1:5000/api/v1/ to visit the API page for locally
hosted application.

Sample Book Response:

```json: books> id=2
{
  "id": 2,
  "author": "Susan Cooper",
  "title": "The Dark Is Rising",
  "year": "1973-01-01T00:00:00",
  "isbn": "1416949658"
}
```

```json: reviews> bookid=2
{
  "total_reviews": 1,
  "reviews": [
    {
      "date": "2021-04-23",
      "ratings": 5,
      "id": 4,
      "comment": "Amazing book",
      "review": "Recommended"
    }
  ]
}
```
