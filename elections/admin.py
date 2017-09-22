from django.contrib import admin
from .models import Election, List, Voter


admin.site.register(Election)
admin.site.register(List)
admin.site.register(Voter)
