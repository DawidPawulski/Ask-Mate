# AskMate
The purpose of this project was to create a forum-like website where users could ask questions, post answers and add comments.

It was my first web application and it involved many challenges. Implementation of user authorization and authentication system. Managing data through relational databases. First lines of HTML code and attemps to make our page alive by giving it some style.

## Setting up
First, create a virtual environment `virtualenv venv` in the project root.

Now install all the packages from `requirements.txt`

`pip install -r requirements.txt`.

You will have to create a database in PostgreSQL and define following environment variables:
- `PSQL_USER_NAME`
- `PSQL_PASSWORD`
- `PSQL_HOST`
- `PSQL_DB_NAME`

In the folder `sample_data` you can find `askmatepart2-sample-data.sql` file. Use it to create tables and fill it with data.

## Specification
Python

Flask

JavaScript

REST API

PostgreSQL
