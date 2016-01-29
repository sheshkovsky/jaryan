from django.conf.urls import include, url
from votes.views import vote_view

urlpatterns = [     
	url(r'^$', vote_view , name='vote'),

]

