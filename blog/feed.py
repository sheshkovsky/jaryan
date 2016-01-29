from django.contrib.syndication.views import Feed
from .models import Entry

class LatestPosts(Feed):
	title = "Jaryan's Blog"
	link =	"/feed/"
	description = "Latest Posts of Jaryan"

	def items(self):
		return Entry.objects.published()[:5]
		