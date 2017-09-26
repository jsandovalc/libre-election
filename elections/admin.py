from django.contrib import admin
from .models import Election, List, Voter, PollingStation, VotingJury, Vote


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Election)
admin.site.register(List)
admin.site.register(Voter)
admin.site.register(PollingStation)
admin.site.register(VotingJury)
admin.site.register(Vote, VoteAdmin)
