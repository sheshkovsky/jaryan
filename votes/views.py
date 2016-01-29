from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from flags.models import Report, REASON_CHOICES
from flags.forms import ReportForm
from links.models import UserProfile
from django.utils import timezone
from datetime import timedelta
import json


from django.contrib.auth.models import User

from votes.models import Vote
from votes.forms import VoteForm
from links.tasks import karma_update

from django.contrib import messages

def vote_view(request, allow_xmlhttprequest=True):
	if request.method == 'POST':

		form = VoteForm(request.POST)

		if form.is_valid():
			content_type = form.cleaned_data['content_type']
			Model = content_type.model_class()
			object_id = form.cleaned_data['object_id']

			try:
				obj = Model.objects.get(id=object_id)
			except ObjectDoesNotExist:
				raise Http404('No %s found to vote.' % (Model))

			user = None
			if request.user.is_authenticated():
				user = request.user

			if str(content_type) in ['text', 'link']:
				submitter = obj.submitter.id
			else:
				submitter = obj.user.id

			vote = form.cleaned_data['vote']

			if 'next' in request.POST:
				next = request.POST['next']
			elif hasattr(obj, 'get_absolute_url'):
				if callable(getattr(obj, 'get_absolute_url')):
					next = obj.get_absolute_url()
				else:
					next = obj.get_absolute_url
			else:
				raise AttributeError('Define get_absolute_url')

			if allow_xmlhttprequest:
				return xmlhttprequest_vote_on_object(request, content_type, Model, object_id, vote)

			voted = Vote.objects.get_for_user(obj, request.user)

			if voted:
				if voted.vote == vote:
					# cancel vote for double click
					Vote.objects.record_vote(obj, request.user, 0, submitter)
				# change direction of vote
				else:
					Vote.objects.record_vote(obj, request.user, vote, submitter)
					# karma_update.delay(submitter, vote*2)
			else:
				print "Not voted", ",", vote
				# record vote directly
				Vote.objects.record_vote(obj, request.user, vote, submitter)
				# karma_update.delay(submitter, vote)

			return HttpResponseRedirect(next)

def json_error_response(error_message):
    return HttpResponse(json.dumps(dict(success=False, error_message=error_message)))


def xmlhttprequest_vote_on_object(request, content_type, Model, object_id, vote):
	if request.method == 'GET':
		return json_error_response('XMLHttpRequest votes can only be made using POST.')
	if not request.user.is_authenticated():
		return json_error_response('Not authenticated.')
	try:
		obj = Model.objects.get(id=object_id)
	except ObjectDoesNotExist:
		return json_error_response('No %s found.' % (Model))

	if str(content_type) in ['text', 'link']:
		submitter = obj.submitter.id
	else:
		submitter = obj.user.id

	voted = Vote.objects.get_for_user(obj, request.user)

	if voted:
		if voted.vote == vote:
			Vote.objects.record_vote(obj, request.user, 0, submitter)
		else:
			Vote.objects.record_vote(obj, request.user, vote, submitter)
	else: 
		Vote.objects.record_vote(obj, request.user, vote, submitter)

	return HttpResponse(json.dumps({
		'success': True,
		'score': Vote.objects.get_score(obj),
	}))


