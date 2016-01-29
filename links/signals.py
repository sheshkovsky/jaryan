from django.db.models.signals import post_save
from django.contrib.auth.models import User
from comments.signals import comment_was_posted


from .models import Link, Post, UserProfile, Follow, Jaryanak
from votes.models import Vote
from comments.models import ThreadedComment
from .tasks import notification_instant, karma_update

def create_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)
# Signal while saving user
post_save.connect(create_profile, sender=User)

def default_j(sender, instance, created, **kwargs):
	if created:
		js = Jaryanak.default_objects.all()
		for j in js:
			f = Follow(user=instance, jaryanak=j)
			f.save()
post_save.connect(default_j, sender=User)


def notify_instant(sender, instance, created, **kwargs):
	if created:
		print "sening notif"
		notification_instant.delay(instance.id)
post_save.connect(notify_instant, sender=Link)


def karma_sig(sender, instance, created, **kwargs):
	if created:
		pk = instance.content_object.submitter.id
		karma_update.delay(pk, 1)
post_save.connect(karma_sig, sender=ThreadedComment)


def vote_own_post(sender, instance, created, **kwargs):
	if created:
		obj = instance.content_object
		user = instance.content_object.submitter
		Vote.objects.record_vote(obj, user, +1, user.id)
post_save.connect(vote_own_post, sender=Post)