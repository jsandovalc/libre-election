from django.db import models


class Election(models.Model):
    """Almost everty other model belongs to an Election."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Elección"
        verbose_name_plural = "Elecciones"


    def __str__(self):
        return f'Elección: {self.name}'


class List(models.Model):
    """A list of candidates."""
    short_description = models.CharField(max_length=50)
    description = models.TextField()

    election = models.ForeignKey('Election', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listas"

    def __str__(self):
        return f"Lista: {self.short_description}"


class Voter(models.Model):
    """A voter for an election."""
    document = models.CharField(max_length=20)

    election = models.ForeignKey('Election', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Votante"
        verbose_name_plural = "Votantes"
        unique_together = (('document', 'election'),)

    def __str__(self):
        return f"Votante: {self.document}"
