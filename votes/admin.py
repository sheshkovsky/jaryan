from django.contrib import admin
from votes.models import Vote

class VoteAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'object', 'vote', 'submit_date')

admin.site.register(Vote, VoteAdmin)

# Register your models here.
