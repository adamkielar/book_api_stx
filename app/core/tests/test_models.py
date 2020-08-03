from django.test import TestCase

from core import models


class ModelTest(TestCase):
    def test_book_str(self):
        """Test the book string representation"""
        book = models.Book.objects.create(
            title="Hobbit czyli Tam i z powrotem",
            authors=["J. R. R. Tolkien"],
            published_date="2004",
            categories=["Baggins, Bilbo (Fictitious character)"],
            average_rating=5,
            ratings_count=2,
        )

        self.assertEqual(str(book), book.title)
