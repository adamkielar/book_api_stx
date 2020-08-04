from rest_framework import viewsets

from core.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Manage following endpoint:
    /books
    /books/<bookid>
    """
    pass
