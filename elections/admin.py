from django.contrib import admin
from .models import Election, List, Voter, PollingStation


admin.site.register(Election)
admin.site.register(List)
admin.site.register(Voter)
admin.site.register(PollingStation)
