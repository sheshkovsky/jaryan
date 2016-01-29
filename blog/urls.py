from django.conf.urls import include, url
from .views import BlogIndex, BlogDetail
from .feed import LatestPosts

urlpatterns = [
	url(r'^$', BlogIndex.as_view(), name="blog"),
	url(r'^feed/$', LatestPosts, name="feed_blog"),
	url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>\S+)$', BlogDetail.as_view(), name="blog_detail"),
]