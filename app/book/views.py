from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['published_date']

    def get_queryset(self):
        queryset = self.queryset
        filter_by_date = self.request.query_params.get('published_date', None)
        if filter_by_date:
            queryset = queryset.filter(published_date=filter_by_date)
        return queryset
