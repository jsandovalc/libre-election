from django.db import models
from django.contrib.auth.models import User


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


class PollingStation(models.Model):
    """A polling stating for an election."""
    name = models.CharField(max_length=30)

    election = models.ForeignKey('Election', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Mesa de votación"
        verbose_name_plural = "Mesas de votación"

    def __str__(self):
        return f"Mesa: {self.name}"


class VotingJury(models.Model):
    """Allows voting to users on a polling station."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    polling_station = models.ForeignKey("PollingStation",
                                        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Jurado de votación"
        verbose_name_plural = "Jurados de votación"

    def __str__(self):
        return f"Jurado: {self.user.username}"


class Vote(models.Model):
    """A vote from a voter. As simple as that."""
    created = models.DateTimeField(auto_now_add=True)

    voter = models.OneToOneField('Voter', on_delete=models.CASCADE)
    polling_station = models.ForeignKey('PollingStation',
                                        on_delete=models.CASCADE)
    list_choice = models.ForeignKey('List', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return f"Vote: {self.voter.document} in {self.polling_station.name}"
