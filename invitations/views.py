from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from links.models import Jaryanak, Membership, Follow
from invitations.models import Invite
from invitations.forms import InviteForm

from django.contrib import messages


is_key_valid = Invite.objects.is_key_valid

def InviteAcceptView(request, key, decision):
	invite = get_object_or_404(Invite, key=key)

	if invite.is_usable():
		if decision == "accept":
			invitee = request.user
			jaryanak = invite.jaryanak
			invite.mark_accepted()
			m = Membership(user=invitee, jaryanak=jaryanak)
			m.save()
			f = Follow(user=invitee, jaryanak=jaryanak)
			f.save()
			return HttpResponseRedirect(reverse('profile', kwargs={'slug': request.user}))
		elif decision == "reject":
			invite.mark_used()
			messages.error(request, "You just rejected the invite.")
			return redirect("home")
		elif decision == "expire":
			invite.mark_expired()
			messages.success(request, "You just cancelled your invitation")
			return redirect("home")
	else:
		return redirect("home")

def InviteCreateView(request, pk, slug):
	template_name = "invitations/invite_form.html"
	success_url = None
	jaryanak = get_object_or_404(Jaryanak, pk=pk)
	remaining_invitations_for_jaryanak = jaryanak.invitations

	if request.method == 'POST':
		form = InviteForm(request.POST)

		if form.is_valid() and remaining_invitations_for_jaryanak:
			inviter = request.user
			invitee = form.cleaned_data["invitee"]
			jaryanak = jaryanak
			if not inviter == invitee and not invitee == jaryanak.admin :
				invited = Invite.objects.filter(invitee__exact=invitee).filter(jaryanak__exact=jaryanak)
				if not invited:
					Invite.objects.create_invitation(inviter, invitee, jaryanak)
					messages.success(request, "You've invited %s to %s successfully" %(invitee, jaryanak))
				else:
					messages.error(request, "You've invited %s to %s before" %(invitee, jaryanak))
			elif inviter == invitee:
				messages.error(request, "You can not invite yourself!")
			elif invitee == jaryanak.admin:
				messages.error(request, "You can not invite Admin to her own jaryanak!")
			return HttpResponseRedirect(success_url or reverse('jaryanak_detail', kwargs={'pk': pk, 'slug': slug}))
	else:
		form = InviteForm()

	return render(request, template_name, {'form':form, 'remaining_invitations_for_jaryanak':remaining_invitations_for_jaryanak, 'jaryanak':jaryanak})


	def get_success_url(self):
		return reverse('jaryanak_detail', kwargs={'pk': pk, 'slug': slug})