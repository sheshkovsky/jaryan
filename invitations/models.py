import os
import random
from hashlib import sha1
from django.db import models
from django.db.models import F
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import timedelta
from django.db.models.signals import post_save
from django.utils import timezone 
from links.models import Jaryanak
from registration.models import SHA1_RE


class InviteManager(models.Manager):
	def get_key(self, invitation_key):
		"""
		Return InvitationKey, or None if it doesn't (or shouldn't) exist.
		"""
		if not SHA1_RE.search(invitation_key):
			return None

		try:
			key = self.get(key=invitation_key)
		except self.model.DoesNotExist:
			return None

		return key

	def is_key_valid(self, invitation_key):
		invitation_key = self.get_key(invitation_key)
		return invitation_key and invitation_key.is_usable()

	def create_invitation(self, inviter, invitee, jaryanak):
		salt = sha1(str(random.random())).hexdigest()[:5]
		key = sha1("%s%s%s" % (timezone.now(), salt, inviter.username)).hexdigest()
		return self.create(key=key, inviter=inviter, invitee=invitee, jaryanak=jaryanak)	

	def remaining_invitations_for_jaryanak(self, jaryanak):
		"""
		Return the number of remaining_invitations_for given jaryanak
		"""
		jaryanak = Jaryanak.objects.get(pk=jaryanak.id)
		return jaryanak.invitations

	def expire_expired_keys(self):
		for key in self.all():
			if key.key_expired():
				self.used = True
				self.status = EXPIRED

class Invite(models.Model):
	key = models.CharField(_('invitation key'), max_length=40)
	created_at = models.DateTimeField(auto_now_add=True)
	inviter = models.ForeignKey(User, related_name='inviter')
	invitee = models.ForeignKey(User, related_name='invitee')
	jaryanak = models.ForeignKey(Jaryanak)
	used = models.BooleanField(default=False)
	PENDING, ACCEPTED, REJECTED, EXPIRED = range(4)
	INVITE_STATUS_CHOICES = (
		(PENDING, 'Pending'),
		(ACCEPTED, 'Accepted'),
		(REJECTED, 'Rejected'),
		(EXPIRED, 'Expired'),
	)
	status 	= models.IntegerField(choices=INVITE_STATUS_CHOICES, default=PENDING)

	objects = InviteManager()

	def __unicode__(self):
		return "Invite from %s, for %s to moderate %s" % (self.inviter, self.invitee, self.jaryanak)

	def is_usable(self):
		return not self.used

	def mark_accepted(self):
		self.used = True
		self.status = 1
		self.save()

	def mark_rejected(self):
		self.used = True
		self.status = 2
		self.save()

	def mark_expired(self):
		self.used = True
		self.status = 3
		self.save()
		Jaryanak.objects.filter(id=self.jaryanak.id).update(invitations=F('invitations')+1)

	def key_expired(self):
		expired = self.created_at + timedelta(days=7) <= timezone.now()
		if expired:
			self.status = 3
			self.save()
		return expired

	def can_send_invite(self):
		return self.jaryanak.admin == self.inviter

	def send_to(self, user):
		""" 
		Send invitation for ``user``
		"""
		subject = render_to_string('invitations/invitation_email_subject.txt',{ 'invite': self })
		subject = ''.join(subject.splitlines())

		message = render_to_string('invitations/invitation_email.txt', { 'invite': self, 'expiration_date': 7})

		send_mail(subject, message, "noreply@jaryan.io", [user.email])
		

def invitation_sent(sender, instance, created, **kwargs):
	if created:
		Jaryanak.objects.filter(id=instance.jaryanak.id).update(invitations=F('invitations')-1)
post_save.connect(invitation_sent, sender=Invite)