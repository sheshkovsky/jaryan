import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction


# New transaction support in Django 1.6
try:
    transaction_atomic = transaction.atomic
except AttributeError:
    transaction_atomic = transaction.commit_on_success

try:
    from django.apps import apps
except ImportError:
    # Django 1.6 or below.
    def is_installed(appname):
        return appname in settings.INSTALLED_APPS
else:
    # Django 1.7 provides an official API, and INSTALLED_APPS may contain non-string values too.
    # However, by checking for settings.INSTALLED_APPS the check can occur before the app registry is ready.
    def is_installed(appname):
        return appname in settings.INSTALLED_APPS #or apps.is_installed(appname)


if is_installed('django.contrib.comments'):
    BASE_APP = 'django.contrib.comments'
    if django.VERSION >= (1,8):
        # Help users migrate their projects easier without having to debug our import errors.
        # The django-contrib-comments package is already installed via setup.py, so changing INSTALLED_APPS is enough.
        raise ImproperlyConfigured("Django 1.8 no longer provides django.contrib.comments.\nUse 'comments' in INSTALLED_APPS instead.")

    # Django 1.7 and below
    from django.contrib import comments as comments
    from django.contrib.comments import get_model, get_form, signals
    from django.contrib.comments.forms import CommentForm
    from django.contrib.comments.models import Comment
    from django.contrib.comments.managers import CommentManager
    from django.contrib.comments.views.comments import CommentPostBadRequest
elif is_installed('comments'):
    BASE_APP = 'comments'
    # as of Django 1.8, this is a separate app.
    import comments
    from comments import get_model, get_form, signals
    from comments.forms import CommentForm
    from comments.models import Comment
    from comments.managers import CommentManager
    from comments.views.comments import CommentPostBadRequest
else:
    raise ImproperlyConfigured("Missing comments or django.contrib.comments in INSTALLED_APPS")


__all__ = (
    'BASE_APP',
    'is_installed',
    'comments',
    'signals',
    'get_model',
    'get_form',
    'CommentForm',
    'Comment',
    'CommentManager',
    'moderator',
    'CommentModerator',
    'CommentPostBadRequest',
)
