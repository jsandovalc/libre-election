from django.contrib import admin
from .models import Election, List, Voter, PollingStation, VotingJury


admin.site.register(Election)
admin.site.register(List)
admin.site.register(Voter)
admin.site.register(PollingStation)
admin.site.register(VotingJury)
