from django.db import models


class Election(models.Model):
    """Almost everty other model belongs to an Election."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
