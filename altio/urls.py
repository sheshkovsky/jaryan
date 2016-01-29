from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.contrib.auth.decorators import login_required as auth
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from links.views import HomeListView, SearchJaryanaks
from links.views import LinkCreateView, LinkDetailView, LinkUpdateView, LinkDeleteView
from links.views import TextCreateView, TextDetailView, TextUpdateView, TextDeleteView
from links.views import JaryanakCreateView, JaryanakListView, JaryanakUpdateView, JaryanakDetailView, JReportsView
from links.views import UserProfileDetailView, UserProfileEditView, UserProfileInvitations, UserProfileReports, FollowView
from links.views import AllReportsView

from links.models import Link, Text
from comments.models import ThreadedComment
# from votes.views import vote_on_object, vote_on_comment




urlpatterns = [
    url(r'^$', HomeListView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^manageeallreports/$', auth(AllReportsView.as_view()), name='all_reports_manager'),

    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^profile/edit/$', auth(UserProfileEditView.as_view()), name="edit_profile"),
    url(r'^profile/(?P<slug>\w+)/invitations/$', auth(UserProfileInvitations.as_view()), name="profile_invites"),
    url(r'^profile/(?P<slug>\w+)/reports/$', auth(UserProfileReports.as_view()), name="profile_reports"),

    url(r'^login/$', "django.contrib.auth.views.login", {"template_name": "login.html"}, name="login"),
    url(r'^logout/$', "django.contrib.auth.views.logout_then_login", name="logout"),

    url(r'^j/list/$', JaryanakListView.as_view(), name='jaryanak'),
    url(r'^j/create/$', auth(JaryanakCreateView.as_view()), name='jaryanak_create'),
    url(r'^j/(?P<pk>\d+)/(?P<slug>[-\w\d\_]+)/$', JaryanakDetailView.as_view(), name='jaryanak_detail'),
    url(r'^j/update/(?P<pk>\d+)/$', auth(JaryanakUpdateView.as_view()), name='jaryanak_update'),
    url(r'^j/(?P<pk>\d+)/reports$', auth(JReportsView.as_view()), name='j_reports'),


    url(r'^links/create/$', auth(LinkCreateView.as_view()), name='link_create'),
    url(r'^links/(?P<pk>\d+)/(?P<slug>[-\w\d\_]+)/$', LinkDetailView.as_view(), name='link_detail'),
    url(r'^links/update/(?P<pk>\d+)/$', auth(LinkUpdateView.as_view()), name='link_update'),
    url(r'^links/delete/(?P<pk>\d+)/$', auth(LinkDeleteView.as_view()), name='link_delete'),

    url(r'^texts/create/$', auth(TextCreateView.as_view()), name='text_create'),
    url(r'^texts/(?P<pk>\d+)/(?P<slug>[-\w\d\_]+)/$', TextDetailView.as_view(), name='text_detail'),
    url(r'^texts/update/(?P<pk>\d+)/$', auth(TextUpdateView.as_view()), name='text_update'),
    url(r'^texts/delete/(?P<pk>\d+)/$', auth(TextDeleteView.as_view()), name='text_delete'),

    # url(r'^vote/$', vote_on_object, name='vote_link'),
    # url(r'^texts/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, text_dict, name='vote_text'),
    # url(r'^comments/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_comment, comment_dict, name='comment-vote'),
    # url(r'^vote/$', vote_on_object, widget_dict, name='vote'),
    # url(r'^vote/$', auth(VoteFormView.as_view()), {"template_name": None}, name='vote'),

    url(r'^invite/', include('invitations.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^report/', include('flags.urls')),
    url(r'^vote/', include('votes.urls')),
    url(r'^follow/jaryank/(?P<pk>\d+)/(?P<slug>[-\w\d\_]+)/$', FollowView, name='follow'),

    url(r'^blog/', include('blog.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^search/$', SearchJaryanaks, name='search'),

    url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^rules/$', views.flatpage, {'url': '/rules/'}, name='rules'),


    # url(r'^tags/$', TagsListView.as_view(), name='tags'),
    # url(r'^tag/(?P<slug>[-\w\d]+)/$', TagsDetailView.as_view(), name='tag_detail'),
    # url(r'^category/(?P<slug>[-\w\d]+)/$', CategoryDetailView.as_view(), name='category_detail'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# link_dict = {
#     'model': Link,
# }

# text_dict = {
#     'model': Text,
#     'template_object_name': None,
#     'allow_xmlhttprequest': True,
# }

# comment_dict = {
#     'model': ThreadedComment,
#     'template_object_name': 'home',
#     'allow_xmlhttprequest': True,
# }

