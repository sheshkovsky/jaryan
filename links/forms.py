from django import forms
from .models import UserProfile, Link, Text, Jaryanak

class UserProfileForm(forms.ModelForm):
    class Meta:
        model 	= UserProfile
        exclude = ('user' , 'karma', 'ip', 'banned_from')

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'title', 'description', 'jaryanak', 'language', 'nsfw_flag']
        widgets = {
            'jaryanak': forms.RadioSelect,
            'language': forms.RadioSelect
        }

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'description', 'jaryanak', 'language', 'nsfw_flag']
        widgets = {
            'jaryanak': forms.RadioSelect,
            'language': forms.RadioSelect
        }

class JaryanakForm(forms.ModelForm):
    class Meta:
        model   = Jaryanak
        exclude = ('slug', 'admin', 'moderators', 'followers', 'created_at', 'is_active', 'invitations')

# from registration.forms import RegistrationForm
# RegistrationForm.base_fields.update(UserProfileForm.base_fields)

# class NewRegistrationForm(RegistrationForm):
#     def save(self, profile_callback=None):
#         UserProfile.objects.get_or_create(
#         	user 	=user, 
#         	picture	=self.cleaned_data['picture'], 
#         	bio		=self.cleaned_data['bio'],
#         	blog 	=self.cleaned_data['blog'])
#         super(NewRegistrationForm, self).save(self, profile_callback)

# class VoteForm(forms.ModelForm):
# 	class Meta:
# 		model = Vote
# 		exclude = ('vote_date',)

# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('comment',)