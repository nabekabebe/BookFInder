DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;

 CREATE TABLE users(
     id SERIAL PRIMARY KEY,
     username VARCHAR(80) NOT NULL,
     email VARCHAR(80) NOT NULL UNIQUE,
     password VARCHAR(40) NOT NULL
 );

CREATE TABLE books(
    id BIGSERIAL PRIMARY KEY,
    isbn TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year TIMESTAMP NOT NULL
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    userId SERIAL NOT NULL REFERENCES users (id),
    bookId BIGINT NOT NULL REFERENCES books (id),
    comment TEXT NOT NULL,
    ratings INTEGER DEFAULT 0 CHECK (ratings >= 0) CHECK (ratings <= 5),
    review TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0,
    reviewedAt DATE NOT NULL DEFAULT CURRENT_DATE
);
