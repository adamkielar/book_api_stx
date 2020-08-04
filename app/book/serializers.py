from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for book object"""
    authors = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'authors',
            'published_date',
            'categories',
            'average_rating',
            'ratings_count',
            'thumbnail'
        )
        read_only_fields = ('id',)
