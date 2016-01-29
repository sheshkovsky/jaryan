from django.db import models
from django.core.urlresolvers import reverse

class EntryQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publish=True)

class Entry(models.Model):
	title 		= models.CharField(max_length=200)
	slug 		= models.SlugField(max_length=200, unique=True)
	body		= models.TextField()
	publish		= models.BooleanField(default=True)
	created 	= models.DateTimeField(auto_now_add=True)
	modified	= models.DateTimeField(auto_now=True)

	objects 	= EntryQuerySet().as_manager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("entry_detail", kwargs={'slug': self.slug})

	class Meta:
			verbose_name = 'Blog Entry'
			verbose_name_plural='Blog Entries'
			ordering = ['-created']