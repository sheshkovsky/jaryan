from __future__ import absolute_import

from celery import shared_task
from links.models import UserProfile

@shared_task
def karma_update(user, k):
	UserProfile.objects.karma_update(user, k)
	print "Karma updated for %s by %s!" %(user, k)