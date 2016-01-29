from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from links.models import Jaryanak


SPAM, VOTE_MANIPULATION, PERSONAL, SEX_ABUSE, BREAKING, OTHER = range(6)
REASON_CHOICES = (
		(SPAM, 'Spam'),
		(VOTE_MANIPULATION, 'Vote Manipulation'),
		(PERSONAL, 'Personal Info'),
		(SEX_ABUSE, 'Abusive'),
		(BREAKING, 'Breaking Jaryan'),
		(OTHER, 'Other'),
	)

PENDING, BAN1, BAN3, BAN10, BAN, UNPUBLISHED, NOACTION, DEACTIVATE = range(8)
REPORT_STATUS_CHOICES = (
	(PENDING, 'Pending'),
	(BAN1, 'Banned for 1 day'),
	(BAN3, 'Banned for 3 days'),
	(BAN10, 'Banned for 10 days'),
	(BAN, 'Banned forever'),
	(UNPUBLISHED, 'Post unpubished'),
	(NOACTION, 'No action needed'),
	(DEACTIVATE, 'User is Deactivated')
	)

class ReportManager(models.Manager):
	def record_report(self, obj, user, jaryanak, reason, ip):
		report, created = Report.objects.get_or_create(
			reporter=user, 
			content_type=ContentType.objects.get_for_model(obj), 
			object_id=obj.pk, 
			jaryanak=jaryanak, 
			reason=reason,
			ip=ip
		)
		report.save()
		return report

	def get_report(self, obj, user):
		if not user.is_authenticated():
			return False
		ctype = ContentType.objects.get_for_model(obj)
		try:
			report = self.filter(content_type=ctype).filter(object_id=obj.id).filter(reporter=user)
		except models.ObjectDoesNotExist:
			report = None
		if report:
			return True
	
	def get_report_for_jarayanak(self, jaryanak):
		return Report.objects.filter(jaryanak__exact=jaryanak)

class BookmarkManager(models.Manager):
	pass

class BaseFlag(models.Model):
	limit = models.Q(app_label='links', model='link') | models.Q(app_label='links', model='text') | models.Q(app_label='comments', model='threadedcomment')
	content_type = models.ForeignKey(ContentType, limit_choices_to = limit)
	object_id = models.PositiveIntegerField()
	object = GenericForeignKey('content_type', 'object_id')
	submit_date = models.DateTimeField(auto_now_add=True)
	ip = models.GenericIPAddressField(null=True)

	class Meta:
		abstract = True

class Report(BaseFlag):
	reporter = models.ForeignKey(User, related_name='reporters')
	reason 	= models.IntegerField(choices=REASON_CHOICES, default=SPAM)
	status 	= models.IntegerField(choices=REPORT_STATUS_CHOICES, default=PENDING)
	jaryanak = models.ForeignKey(Jaryanak, related_name='jaryanak')
	moderater = models.ForeignKey(User, related_name='moderator', null=True)
	date_moderated = models.DateTimeField(null=True, blank=True)

	objects = ReportManager()

	class Meta:
		db_table = 'reports'
		ordering =['submit_date']
        # One vote per user per object
        unique_together = (('reporter', 'content_type', 'object_id'),)

	def __unicode__(self):
		return "%s reported %s" %(self.reporter, self.object)

class Bookmark(BaseFlag):
	user = models.ForeignKey(User, related_name='bookmarker')

	objects = BookmarkManager()

	class Meta:
		db_table = 'bookmarks'
		ordering = ['submit_date']
		unique_together = ('user', 'content_type', 'object_id')

	def __unicode__(self):
		return "%s bookmarked %s" %(self.user, self.object)