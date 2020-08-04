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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_date']

    def get_queryset(self):
        queryset = self.queryset
        filter_by_date = self.request.query_params.get('published_date', None)
        filter_by_author = self.request.GET.getlist('author')
        if filter_by_date:
            queryset = queryset.filter(published_date=filter_by_date)
        if filter_by_author:
            author_list = [author.strip('"') for author in filter_by_author]
            queryset = queryset.filter(authors__contained_by=author_list)
        return queryset
