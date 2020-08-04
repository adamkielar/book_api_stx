from rest_framework import viewsets

from core.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Manage following endpoint:
    /books
    /books/<bookid>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
