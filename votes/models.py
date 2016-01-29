from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from votes.tasks import karma_update

from django.utils import timezone

SCORES = (
	(+1, '+1'),
	(-1, '-1'),
)

class VoteManager(models.Manager):
	def get_score(self, obj):
		ctype = ContentType.objects.get_for_model(obj)
		result = self.filter(
			content_type=ctype,
			object_id=obj._get_pk_val()
		).aggregate(
			score=Sum('vote'),
			num_votes=Count('vote')
		)

		if result['score'] is None:
			result['score'] = 0
		return result

	def record_vote(self, obj, user, vote, submitter):
		print "passing vote is:", vote
		if vote not in (+1, 0 , -1):
			raise ValueError('Invalid vote! (must be +1/0/-1')
		ctype = ContentType.objects.get_for_model(obj)
		try:
			v = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val())
			if vote == 0:
				if v.vote == 1:
					# deleting +1 vote
					karma_update.delay(submitter, -1)
				else:
					# deleting -1 vote
					karma_update.delay(submitter, +1)
				v.delete()
			else:
				v.vote = vote
				v.save()
				# updating karma for changing vote
				karma_update.delay(submitter, 2*vote)

		except models.ObjectDoesNotExist:
			if vote == 0:
				return
			self.create(user=user, content_type=ctype, object_id=obj._get_pk_val(), vote=vote)
			# updating karma on submitting vote
			karma_update.delay(submitter, vote)


	def get_for_user(self, obj, user):
		if not user.is_authenticated():
			return None
		ctype = ContentType.objects.get_for_model(obj)
		try:
			vote = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val())
		except models.ObjectDoesNotExist:
			vote = None
		return vote

class Vote(models.Model):
	user = models.ForeignKey(User, related_name='voter')
	limit = models.Q(app_label='links', model='link') | models.Q(app_label='links', model='text') | models.Q(app_label='comments', model='threadedcomment')
	content_type = models.ForeignKey(ContentType, limit_choices_to = limit)
	object_id = models.PositiveIntegerField()
	object = GenericForeignKey('content_type', 'object_id')
	vote = models.SmallIntegerField(choices=SCORES)
	submit_date = models.DateTimeField(editable=False, auto_now_add=True)

	objects = VoteManager()

	class Meta:
		db_table = 'votes'
		ordering =['submit_date']
        unique_together = (('user', 'content_type', 'object_id'),)

	def __unicode__(self):
		return "%s: voted %s on %s" %(self.user, self.vote, self.object)

	def is_upvote(self):
		return self.vote == 1

	def is_downvote(self):
		return self.vote == -1