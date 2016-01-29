from django import forms
from django.contrib.contenttypes.models import ContentType

SPAM, VOTE_MANIPULATION, PERSONAL, SEX_ABUSE, BREAKING, OTHER = range(6)
REASON_CHOICES = (
		(SPAM, 'Spam'),
		(VOTE_MANIPULATION, 'Vote Manipulation'),
		(PERSONAL, 'Personal Info'),
		(SEX_ABUSE, 'Abusive'),
		(BREAKING, 'Breaking Jaryan'),
		(OTHER, 'Other'),
	)

class ReportForm(forms.Form):
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content_type = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=ContentType.objects.all())
	reason = forms.ChoiceField(choices=REASON_CHOICES, widget=forms.RadioSelect)

	# def clean(self):
	# 	content_type = self.cleaned_data['content_type']
	# 	Model = content_type.model_class()
	# 	id = self.cleaned_data['object_id']
	# 	try:
	# 		obj = Model.objects.get(id=id)
	# 	except Model.DoesNotExist:
	# 		raise forms.ValidationError("No such %s object with id %s" % (Model, id))

	# 	self.cleaned_data['object'] = obj
	# 	return self.cleaned_data

