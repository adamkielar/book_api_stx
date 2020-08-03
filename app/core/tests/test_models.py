from django.test import TestCase

from core import models


class ModelTest(TestCase):
    def test_book_str(self):
        """Test the book string representation"""
        book = models.Book.objects.create(
            title="Hobbit czyli Tam i z powrotem"
        )

        self.assertEqual(str(book), book.title)
