from django.contrib import admin

from invitations.models import Invite

class InviteAdmin(admin.ModelAdmin):
	list_display = ('id', 'inviter', 'invitee', 'jaryanak', 'created_at', 'status', 'used', 'key_expired')

admin.site.register(Invite, InviteAdmin)
