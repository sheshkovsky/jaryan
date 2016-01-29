from django.conf.urls import include, url
from django.conf import settings

from django.views.generic.base import TemplateView

from invitations.views import InviteCreateView, InviteAcceptView

urlpatterns = [
    url(r'^j/(?P<pk>\d+)/(?P<slug>[-\w\d\_]+)/invite$', InviteCreateView, name='invite_moderator'),
    url(r'^accept/(?P<key>[-\w\d\_]+)/(?P<decision>accept|reject|expire)$', InviteAcceptView, name='invite_accept_moderator'),

    # url(r'^invite/complete/$',
    #             direct_to_template,
    #             {'template': 'invitation/invitation_complete.html'},
    #             name='invitation_complete'),

    # url(r'^invited/(?P<invitation_key>\w+)/$', 
    #             invited,
    #             name='invitation_invited'),
    # url(r'^register/$',
    #             register,
    #             { 'backend': 'registration.backends.default.DefaultBackend' },
    #             name='registration_register'),
]
