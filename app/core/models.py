from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models


class Book(models.Model):
    """Book object"""
    title = models.CharField(max_length=255)
    authors = ArrayField(models.CharField(max_length=255))
    published_date = models.CharField(max_length=10, blank=True)
    categories = ArrayField(
        models.CharField(max_length=255, null=True, blank=True),
        blank=True,
        null=True
    )
    average_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(5)]
    )
    ratings_count = models.PositiveIntegerField(blank=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

