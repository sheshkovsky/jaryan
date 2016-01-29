from django import forms
from invitations.models import Invite

class InviteForm(forms.ModelForm):
    class Meta:
        model 	= Invite
        exclude = ('key' , 'inviter', 'created_at', 'jaryanak', 'used', 'status')