from django.conf.urls import include, url
from flags.views import report_view, report_action

urlpatterns = [     
	url(r'^$', report_view, name='report'),
    url(r'^(?P<pk>\d+)/(?P<action>\d+)/$', report_action, name='report_action'),

]

