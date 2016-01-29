from django.db.models import Q
from links.models import Post
from comments.models import ThreadedComment as comments
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages

KARMA_LOW = 100
KARMA_MEDIUM = 1000
KARMA_HIGH = 5000 

INTERVAL_LOW = 3600
INTERVAL_MEDIUM = 360
INTERVAL_HIGH = 36 

COMMENT_PER_INTERVAL = 20
COMMENT_MAX = 80


def allowed_to_comment(user):
	karma = user.userprofile.karma
	now = timezone.now()

	time_threshold = now - timedelta(seconds=3600)
	comments_number = comments.objects.filter(Q(user=user) and Q(submit_date__gt=time_threshold)).count()

	if karma < KARMA_HIGH:
		if comments_number > COMMENT_PER_INTERVAL:
			return False
		else: 
			return True
	else:
		if comments_number > COMMENT_MAX:
			return False
		else:
			return True

def allowed_to_post(request, user):
	karma = user.userprofile.karma
	print karma
	now = timezone.now()
	
	try:
		posted = Post.objects.filter(post__submitter__exact=user).latest('submit_date')
		diff = now - posted.submit_date
		diff = diff.seconds
	except: 
		diff = INTERVAL_LOW + 1

	print diff 

	if karma < KARMA_LOW:
		result = diff > INTERVAL_LOW
		if not result:
			messages.success(request, 'Please try in an hour!')
		return result
	elif karma > KARMA_LOW and karma < KARMA_HIGH:
		result = diff > INTERVAL_MEDIUM
		if not result:
			messages.success(request, 'Please try in ten minutes!')
		return result
	else:
		result = diff > INTERVAL_HIGH
		if not result:
			messages.warning(request, 'Please try in 30 sec')
		return result

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

