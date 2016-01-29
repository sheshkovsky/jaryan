from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404
from flags.models import Report, REASON_CHOICES
from flags.forms import ReportForm
from links.models import UserProfile
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from links.utils import get_client_ip

from links.tasks import remove_ban_task

from django.contrib import messages

def report_view(request):
	if request.method == 'POST':
		#create a form instance
		form = ReportForm(request.POST)

		if form.is_valid():
			#process the data in form.cleaned_data as required
			content_type = form.cleaned_data['content_type']
			Model = content_type.model_class()
			id = form.cleaned_data['object_id']
			obj = Model.objects.get(id=id)

			try:
				jaryanak = obj.jaryanak
			except:
				# for comments
				jaryanak = obj.content_object.jaryanak

			user = None
			if request.user.is_authenticated():
				user = request.user

			reason = form.cleaned_data['reason']

			ip = get_client_ip(request)

			reported = Report.objects.get_report(obj, user)
			
			if reported:
				messages.warning(request, "You've reported this before!")
			else:
				Report.objects.record_report(obj, user, jaryanak, reason, ip)
				messages.success(request, "Thank you for reporting this object!")

			if 'next' in request.POST:
				next = request.POST['next']
			elif hasattr(obj, 'get_absolute_url'):
				if callable(getattr(obj, 'get_absolute_url')):
					next = obj.get_absolute_url()
				else:
					next = obj.get_absolute_url
			else:
				raise AttributeError('Define get_absolute_url')

			return HttpResponseRedirect(next)
		else:
			form = ReportForm()
		return render(request, 'flags/report_form.html', {'form': form, 'reasons':REASON_CHOICES})


def report_action(request, pk, action):
	# get report
	report = get_object_or_404(Report, pk=pk)
	ctype = report.content_type
	Model = ctype.model_class()
	id = report.object_id
	obj = Model.objects.get(id=id)

	user_id = obj.submitter.id
	user_to_ban = User.objects.get(id=user_id)

	jaryanak = obj.jaryanak

	if request.user.is_authenticated():
		if request.user==jaryanak.admin or request.user in jaryanak.moderators.all() or request.user.is_superuser:
			report.status = action
			report.moderator = request.user
			report.moderated = timezone.now()
			report.save()

			if action=="1":
				user_to_ban.userprofile.banned_from.add(jaryanak)
				in_one_day = timezone.now() + timedelta(days=1) 
				remove_ban_task.apply_async(args=[user_id, jaryanak.id], eta=in_one_day)
				messages.success(request, "You've banned the user for one day")

			elif action=="2":
				user_to_ban.userprofile.banned_from.add(jaryanak)
				in_three_days = timezone.now() + timedelta(days=3) 
				remove_ban_task.apply_async(args=[user_id, jaryanak.id], eta=in_three_days)
				messages.success(request, "You've banned the user for three days")


			elif action=="3":
				user_to_ban.userprofile.banned_from.add(jaryanak)
				in_ten_days = timezone.now() + timedelta(days=10) 
				remove_ban_task.apply_async(args=[user_id, jaryanak.id], eta=in_ten_days)
				messages.success(request, "You've banned the user for ten days")


			elif action=="4":
				user_to_ban.userprofile.banned_from.add(jaryanak)
				messages.success(request, "You've banned the user from this Jaryan")

			elif action=="5":
				obj.published = False
				obj.save()
				messages.success(request, "You've unpublished this post")

			elif action=="7":
				if request.user.is_superuser:
					user_to_ban.is_active = False
					user_to_ban.save()
					# send email to inform he has been deactivated
					messages.success(request, "You've deactivated user!")



		if 'next' in request.REQUEST:
			next = request.REQUEST['next']
		elif hasattr(jaryanak, 'get_absolute_url'):
			if callable(getattr(jaryanak, 'get_absolute_url')):
				next = jaryanak.get_absolute_url()
			else:
				next = jaryanak.get_absolute_url
		else:
			raise AttributeError('Define get_absolute_url')

		return HttpResponseRedirect(next)
	else:

		return redirect('home')



	# get object

	#
