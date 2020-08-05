import requests

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from core.models import Book


class Command(BaseCommand):
    """Populate database with books from url"""

    def handle(self, *args, **option):
        self.stdout.write('Fetching data from URL...')
        payload = {'q': 'Hobbit'}
        get_books = requests.get(
            url="https://www.googleapis.com/books/v1/volumes",
            params=payload
        )
        books = get_books.json()
        books = books['items']

        if books:
            for book in books:
                book = book['volumeInfo']
                try:
                    Book.objects.get_or_create(
                        title=book.get('title'),
                        authors=book.get('authors'),
                        published_date=book.get('publishedDate')[:4],
                        categories=book.get('categories', list()),
                        average_rating=book.get('averageRating', 0),
                        ratings_count=book.get('ratingsCount', 0),
                        thumbnail=book['imageLinks'].get('thumbnail')
                    )
                except IntegrityError:
                    self.stdout.write('Duplicate entries')
                    continue
                except KeyError as KeyErrorDesc:
                    self.stdout.write('Book is missing data')
                    print(KeyErrorDesc)
                    continue

        self.stdout.write(self.style.SUCCESS('Books added to database!'))
