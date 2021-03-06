import json
import os

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book

from book.serializers import BookSerializer

BOOKS_URL = reverse('book:book-list')
BOOKS_UPDATE_URL = reverse('book:db-db')
TEST_DATA = os.path.join(os.path.dirname(__file__), 'books_list.json')


def detail_url(book_id):
    """Return book detail url"""
    return reverse('book:book-detail', args=[book_id])


class BookApiTest(TestCase):
    """Test book api"""

    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(
            title="Hobbit czyli Tam i z powrotem",
            authors=["J. R. R. Tolkien"],
            published_date="2004",
            categories=["Baggins, Bilbo (Fictitious character)"],
            average_rating=5,
            ratings_count=2,
        )
        self.book2 = Book.objects.create(
            title="Exploring J.R.R. Tolkien's The Hobbit",
            authors=["Corey Olsen"],
            published_date="2012",
            categories=["Literary Criticism"],
            average_rating=4,
            ratings_count=8,
        )

    def test_retrieve_books(self):
        """Test retrieving a list of books"""
        response = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by('-title')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_book_published_date(self):
        """Test filtering books by published date"""
        book1 = self.book1
        book2 = self.book2

        response = self.client.get(BOOKS_URL, {'published_date': '2004'})
        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_book_by_author(self):
        """Test filtering books by authors"""
        book1 = self.book1
        book2 = self.book2

        response = self.client.get(BOOKS_URL, {'author': 'J. R. R. Tolkien'})
        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_book_detail_view(self):
        """Test viewing a book detail"""
        book = Book.objects.create(
            title="The Hobbit, Or, There and Back Again",
            authors=["John Ronald Reuel Tolkien"],
            published_date="1982",
            categories=["FICTION"],
            average_rating=4,
            ratings_count=2649,
        )
        url = detail_url(book.id)
        response = self.client.get(url)
        serializer = BookSerializer(book)

        self.assertEqual(response.data, serializer.data)


class BookUpdateApiTest(TestCase):
    """Test update Book model with external data"""

    def setUp(self):
        self.client = APIClient()
        self.books_list = open(TEST_DATA)
        self.books = json.load(self.books_list)
        self.books = self.books['items']

    def tearDown(self):
        self.books_list.close()

    def test_retrieve_data_from_file(self):
        """Test to check if data are available"""
        self.assertTrue(self.books)

    def test_update_database_with_books(self):
        """Test updating database with books from file"""
        for book in self.books:
            book = book['volumeInfo']
            payload = {
                'title': book.get('title'),
                'authors': book.get('authors'),
                'published_date': book.get('publishedDate')[:4],
                'categories': book.get('categories', list()),
                'average_rating': book.get('averageRating', 0),
                'ratings_count': book.get('ratingsCount', 0),
                'thumbnail': book['imageLinks'].get('thumbnail')
            }
            response = self.client.post(BOOKS_UPDATE_URL, payload)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        books_in_db = Book.objects.values()[:1].get()
        self.assertIn('title', books_in_db)
