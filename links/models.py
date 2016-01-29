# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.utils.text import slugify
from django.db.models import F
from urlparse import urlparse
from pyfav import get_favicon_url
from thumbs import ImageWithThumbsField
from slugify import slugify_persian
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from django.utils.translation import ugettext_lazy as _


class PostManager(models.Manager):
	def update_rank_score(self, post_id, new_score):
		self.filter(id=post_id).update(rank_score=new_score)

class LinkManager(models.Manager):
	def vote_up(self, pk, increment=True):
		if increment: 
			self.filter(id=pk).update(up_votes=F('up_votes')+1)
		else:
			self.filter(id=pk).update(up_votes=F('up_votes')-1)

	def vote_down(self, pk, increment=True):
		if increment:
			self.filter(id=pk).update(down_votes=F('down_votes')+1)
		else:
			self.filter(id=pk).update(down_votes=F('down_votes')-1)

	def update_rank_score(self, object_id, new_score):
		self.filter(id=object_id).update(rank_score=new_score)

	# Link.objects.daily(j)
	def daily(self, jaryanak):
		return Link.objects.filter(jaryanak__exact=jaryanak, submit_date__gte=timezone.now()-timedelta(days=1))

	def weekly(self, jaryanak):
		return Link.objects.filter(jaryanak__exact=jaryanak, submit_date__gte=timezone.now()-timedelta(days=7))

class TextManager(models.Manager):
	def update_rank_score(self, object_id, new_score):
		self.filter(id=object_id).update(rank_score=new_score)

# class LinkVoteCountManager(models.Manager):
# 	def get_queryset(self):
# 		return super(LinkVoteCountManager, self).get_queryset().filter(votes__vote_type=0).annotate(ups=Count('votes')).order_by('-ups')


class DefaultJaryanaksManager(models.Manager):
	def get_queryset(self):
		return super(DefaultJaryanaksManager, self).get_queryset()[:10]

class JaryanakManager(models.Manager):
	def get_for_user(self, user):
		if not user or user.is_anonymous():
			return None
		js = []
		for j in self.get_queryset():
			if user in j.moderators:
				print "yes"

class Language(models.Model):
	name 		= models.CharField(max_length=50)
	slug 		= models.SlugField(unique=True)

	def __unicode__(self):
		return self.name

class FollowManager(models.Manager):
	def get_for_user(self, user, jaryanak):
		if not user or user.is_anonymous():
			return False
		# try:
		# 	followed = self.get(Follow, user=user, jaryanak=jaryanak)
		# except Follow.DoesNotExist:
		# 	followed = False
		qs = self.filter(user=user)
		followed = qs.filter(jaryanak=jaryanak)
		return followed

class UserManager(models.Manager):
	def karma_update(self, pk, k):
		self.filter(id=pk).update(karma=F('karma')+k)

	def ban_add(self, pk, j):
		self.filter(id=pk).banned_from.add(j)
		
	def ban_remove(slef, pk, j):
		self.filter(id=pk).banned_from.remove(j)



class Jaryanak(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(max_length=400, blank=True)
	logo = ImageWithThumbsField(upload_to='images/logo_pictures/', sizes=((250,250),(50,50),(15,15)), blank=True)
	admin = models.ForeignKey(User, related_name='admin')
	moderators = models.ManyToManyField(User, through='Membership', related_name='moderateors')
	followers = models.ManyToManyField(User, through='Follow', related_name='followers')
	invitations = models.PositiveIntegerField(default=10)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	objects 	= JaryanakManager()
	default_objects = DefaultJaryanaksManager()

	def __unicode__(self):
			return self.name

	def get_absolute_url(self):
		return reverse("jaryanak_detail", kwargs={"pk": str(self.id), "slug": self.slug })

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify_persian(self.name)
		super(Jaryanak, self).save(*args, **kwargs)

class Membership(models.Model):
	user = models.ForeignKey(User)
	jaryanak = models.ForeignKey(Jaryanak)
	date_joined = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
	user = models.ForeignKey(User)
	jaryanak = models.ForeignKey(Jaryanak)
	date_joind = models.DateTimeField(auto_now_add=True)

	objects = FollowManager()

	def __unicode__(self):
		return "%s follows %s" %(self.user, self.jaryanak)

class Thread(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	jaryans = models.ManyToManyField(Jaryanak, related_name='jaryans')

	def __unicode__(self):
		return self.name

class Post(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	submit_date = models.DateTimeField(null=True)
	rank_score = models.FloatField(default=0.0)

	objects = PostManager()

	class Meta:
		ordering = ['-submit_date']

	def __unicode__(self):
		return "{0} - {1} - {2}".format(self.content_type, self.content_object, self.submit_date.date())

# can use a property to get rank score too
	@property	
	def is_link(self):
		return self.content_type.model == "link"

	@property
	def is_text(self):
		return self.content_type.model == "text"

	@property
	def update_object_rank_score(self, new_score):
	     self.content_object.rank_score = new_score

	@property
	def jaryanak(self):
	    return self.content_object.jaryanak

	@property
	def is_nsfw(self):
		return self.content_object.nsfw_flag

	@property
	def is_published(self):
	    return self.content_object.published
	

def create_post(sender, instance, created, **kwargs):
	content_type = ContentType.objects.get_for_model(instance)
	if created:
		try:
			p = Post.objects.get(content_type=content_type, object_id=instance.id)
		except Post.DoesNotExist:
			p = Post(content_type=content_type, object_id=instance.id, submit_date=instance.submit_date, rank_score=instance.rank_score)
		p.save()

class Base(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200, db_index=True)
	jaryanak = models.ForeignKey(Jaryanak, default=1)
	language = models.ForeignKey(Language, default=1)

	published = models.BooleanField(default=True)
	submitter = models.ForeignKey(User)
	submit_date	= models.DateTimeField(auto_now_add=True)
	submitter_ip = models.GenericIPAddressField(null=True)

	modified = models.BooleanField(default=False)
	modify_date = models.DateTimeField(auto_now=True)
	modifier_ip = models.GenericIPAddressField(null=True)

	rank_score = models.FloatField(default=0.0)
	nsfw_flag = models.BooleanField(default=False)
	posts = GenericRelation(Post, related_query_name='post')

	# up_votes 	= models.PositiveIntegerField(default=0, blank=True, db_index=True)
	# down_votes 	= models.PositiveIntegerField(default=0, blank=True, db_index=True)

	class Meta:
		abstract = True

class Link(Base):
	url	= models.URLField("URL")
	description = models.TextField(max_length=500)
	domain = models.CharField(max_length=50)
	favicon = models.URLField(blank=True)
	modifier = models.ForeignKey(User, related_name='link_modifier', null=True)
	# post = GenericRelation(Post, related_query_name='link')

	# with_votes = LinkVoteCountManager()
	objects = LinkManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("link_detail", kwargs={"pk": str(self.id), "slug": self.slug })

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify_persian(self.title)
		if not self.id:
			self.submite_date = timezone.now()
		self.update_time = timezone.now()
		parsed_uri 	= urlparse(self.url)
		self.domain = '{uri.netloc}'.format(uri=parsed_uri)
		super(Link, self).save(*args, **kwargs)
post_save.connect(create_post, sender=Link)

class Text(Base):
	description = models.TextField(max_length=1000)
	# post = GenericRelation(Post, related_query_name='text')
	modifier = models.ForeignKey(User, related_name='text_modifier', null=True)

	# favicon = models.ImageField(upload_to='/images', default="/")

	objects = TextManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("text_detail", kwargs={"pk": str(self.id), "slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify_persian(self.title)
		if not self.id:
			self.submite_date = timezone.now()
		self.update_time = timezone.now()
		super(Text, self).save(*args, **kwargs)
post_save.connect(create_post, sender=Text)

class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	bio	= models.TextField(max_length=500, blank=True)
	blog = models.URLField(blank=True)
	picture = ImageWithThumbsField(upload_to='images/profile_pictures/', sizes=((150,150),(75,75),(15,15)), blank=True)
	karma = models.IntegerField(default=1)
	date_joined = models.DateTimeField(auto_now_add=True)
	ip = models.GenericIPAddressField(null=True)
	nsfw_flag = models.BooleanField(default=False)

	INSTANTLY, DAILY, WEEKLY, NEVER = range(4)
	NOTIFY_PERIOD_CHOICES = (
		(INSTANTLY, 'Instantly'),
		(DAILY, 'Daily'),
		(WEEKLY, 'Weekly'),
		(NEVER, 'Never'),
	)
	notify_me 	= models.IntegerField(choices=NOTIFY_PERIOD_CHOICES, default=INSTANTLY)
	banned_from = models.ManyToManyField(Jaryanak, blank=True, related_name='banned_jaryan')

	objects = UserManager()

	def __unicode__(self):
		return "%s's profile" % self.user

	def is_banned(self, jaryanak):
		return jaryanak in self.banned_from.all()



# class Vote(models.Model):
#     # Post statuses.
#     UP, DOWN = range(2)
#     TYPE_CHOICES = [(UP, "Upvote"), (DOWN, "DownVote")]

#     voter = models.ForeignKey(User)
#     link = models.ForeignKey(Link, related_name='votes')
#     vote_type = models.IntegerField(choices=TYPE_CHOICES, db_index=True)
#     vote_date = models.DateTimeField(db_index=True, auto_now=True)

#     def __unicode__(self):
#         return "%s voted %s a %s" % (self.voter.username, self.link.title, self.vote_type)

#class Comment(models.Model):
# 	user 	= models.ForeignKey(User)
# 	link 	= models.ForeignKey(Link, related_name='comments')
# 	comment 		= models.TextField(max_length=400)
# 	submit_date 	= models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return "%s commented %s on %s" %(self.user.username, self.comment[:50], self.link.title)

# def is_following(self, user, instance):
#         """
#         Check if a user is following an instance.
#         """
#         if not user or user.is_anonymous():
#             return False
#         queryset = self.for_object(instance)
#         return queryset.filter(user=user).exists()


