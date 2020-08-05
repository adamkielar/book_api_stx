import requests

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.utils import IntegrityError

from core.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Manage following endpoint:
    /books
    /books/<bookid>
    """
    allowed_methods = ['GET']
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_date']

    def get_queryset(self):
        queryset = super(BookViewSet, self).get_queryset()
        filter_by_date = self.request.query_params.get('published_date', None)
        filter_by_author = self.request.GET.getlist('author')
        if filter_by_date:
            queryset = queryset.filter(published_date=filter_by_date)
        if filter_by_author:
            author_list = [author.strip('"') for author in filter_by_author]
            queryset = queryset.filter(authors__contained_by=author_list)
        return queryset


class BookUpdateViewSet(viewsets.ModelViewSet):
    """
    Manage endpoint to fetch and update book list
    /db
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_books_from_url(self):
        payload = {'q': 'war'}
        get_books = requests.get(
            url="https://www.googleapis.com/books/v1/volumes",
            params=payload
        )
        books = get_books.json()
        books = books['items']
        return books

    def create_update_books(self, books):
        for book in books:
            book = book['volumeInfo']
            try:
                Book.objects.update_or_create(
                    title=book.get('title'),
                    authors=book.get('authors'),
                    published_date=book.get('publishedDate')[:4],
                    categories=book.get('categories', list()),
                    average_rating=book.get('averageRating', 0),
                    ratings_count=book.get('ratingsCount', 0),
                    thumbnail=book['imageLinks'].get('thumbnail')
                )
            except IntegrityError:
                return Response({'message': 'Duplicate entries'})
            except KeyError:
                return Response({'message': 'Book is missing data'})

    @action(methods=['GET', 'POST'], detail=False, url_path='db')
    def db(self, request):
        books = self.get_books_from_url()
        if books:
            self.create_update_books(books)
            return Response(
                {'message': 'Database updated with new books!'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'External service with books unavailable!'},
            status=status.HTTP_400_BAD_REQUEST
        )
