from django.db import models


class Election(models.Model):
    """Almost everty other model belongs to an Election."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class List(models.Model):
    """A list of candidates."""
    short_description = models.CharField(max_length=50)
    description = models.TextField()

    election = models.ForeignKey('Election', on_delete=models.CASCADE)
