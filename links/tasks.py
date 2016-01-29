from __future__ import absolute_import

from celery import shared_task
from .models import Link, Post, Jaryanak, UserProfile
from votes.models import Vote
from pyfav import get_favicon_url
from datetime import datetime, timedelta
from math import log
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMultiAlternatives

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from links.models import UserProfile
from django.contrib.auth.models import User

# from links.messaging import process_clicks

# from celery.task import PeriodicTask
# class ProcessClicksTask(PeriodicTask):
# 	run_every = timedelta(seconds=5)

# 	def run(self, **kwargs):
# 		process_clicks()

@shared_task
def remove_ban_task(user_id, jaryanak_id):
	j = Jaryanak.objects.get(id=jaryanak_id)
	user = User.objects.get(id=user_id)
	user.userprofile.banned_from.remove(j)
	print "%s removed from %s banned_from's " %(j, user)

@shared_task
def karma_update(user, k):
	UserProfile.objects.karma_update(user, k)
	print "Karma updated!"

@shared_task
def ranker():
	object_list = Post.objects.all()
	for post in object_list:
		score_dict = Vote.objects.get_score(post.content_object)
		s = score_dict['score']
		order = log(max(abs(s), 1), 10)
		if s > 0:
			sign=1
		elif s < 0:
			sign = -1
		else:
   			sign = 0
		epoch = datetime(1970, 1, 1)
		today = datetime.today()
		td = today - epoch
		epoch_seconds =  td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
		seconds = epoch_seconds - 1134028003
		rank_score = round(order + sign * seconds / 45000, 7)
		# set rank_score on the object (link/text)
		Post.objects.update_rank_score(post.id, rank_score)
		Model = post.content_type.model_class()
		Model.objects.update_rank_score(post.content_object.id, rank_score)

@shared_task
def get_favicon(pk):
	sc = Link.objects.get(pk=pk)
	sc.favicon = get_favicon_url(sc.url)
	sc.save()

@shared_task
def notification_instant(id):
	link = Link.objects.get(pk=id)
	jaryanak = link.jaryanak
	# retrieve all followers of the jaryanak who want to receive notifications instantly
	recipient_list = jaryanak.followers.all().filter(userprofile__notify_me=0).values_list('email', flat=True)
	subject, from_email = 'New link posted in %s' % jaryanak, 'noreply@jaryan.io'
	text_content = 'This is an important message.'
	html_content = '<p>This is an <strong>important</strong> message.</p>'
	msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

@shared_task
def notification_daily():
	js = Jaryanak.objects.all()
	for j in js:
		# retrieve all links posted last 24 hours in this jaryanak
		links = Link.objects.daily(j) 
		# retrieve all followers of the jaryanak who want to receive notifications instantly
		recipient_list = j.followers.all().filter(userprofile__notify_me=1).values_list('email', flat=True)
		subject, from_email = 'New links posted in %s' % j, 'noreply@jaryan.io'
		text_content = 'This is an important message.'
		html_content = '<p>This is an <strong>important</strong> message.</p>'
		msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
		msg.attach_alternative(html_content, "text/html")
		msg.send()	
