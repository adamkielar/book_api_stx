from django.contrib.postgres.fields import ArrayField
from django.db import models


class Book(models.Model):
    """Book object"""
    title = models.CharField(max_length=255)
    authors = ArrayField(models.CharField(max_length=255))
    published_date = models.CharField(max_length=10, blank=True)
    categories = ArrayField(
        models.CharField(max_length=255, null=True, blank=True),
        null=True,
        blank=True,
    )
    average_rating = models.PositiveSmallIntegerField(blank=True, default=0)
    ratings_count = models.PositiveIntegerField(blank=True, default=0)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
