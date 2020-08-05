# Book REST Api | Django REST Framework
[![Build Status](https://travis-ci.org/adamkielar/book_api_stx.svg?branch=master)](https://travis-ci.org/adamkielar/book_api_stx)

# Description
REST Api to list books.

Deployment version on feature/deploy branch

## Endpoints

- GET /books /books?published_date=2004, /books?sort=-published_date
- GET /books?author="J. R. R. Tolkien"
- GET /books/<bookId>
- POST /db - fetch data from external url and update database

# How to use:

Clone this repository.

Docker:
- docker-compose up
