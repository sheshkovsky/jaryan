from django import forms
from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin

from links.models import Link, Text, Post, UserProfile, Jaryanak, Membership, Follow
from links.forms import LinkForm, TextForm, UserProfileForm, JaryanakForm
from links.tasks import get_favicon
from links.utils import allowed_to_post, get_client_ip
from comments.models import ThreadedComment
from invitations.models import Invite
from votes.models import Vote
from flags.models import Report, REASON_CHOICES
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib import messages

class HomeListView(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-rank_score')
    paginate_by = 10

    # def get_queryset(self):

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['followed_jaryanaks'] = Jaryanak.objects.filter(followers__exact=self.request.user)
        else:
            context['followed_jaryanaks'] = Jaryanak.objects.all()
        return context

    # model = Link
    # queryset    = Link.objects.all().order_by('-rank_score')
    # # queryset    = Link.with_votes.all()
    # paginate_by = 10

class LinkCreateView(CreateView):
    model       = Link
    form_class  = LinkForm
    template_name = "links/link_form.html"

    def form_valid(self, form):
    # REMOVE "NOT" IN PRODUCTION!!
        if allowed_to_post(self.request, self.request.user):
            f = form.save(commit=False)
            f.submitter = self.request.user
            f.ip = get_client_ip(self.request)
            if not f.submitter.userprofile.is_banned(f.jaryanak):
                f.save()
                get_favicon.delay(f.pk)
                messages.success(self.request, 'Your Link has been sent')
            else:
                messages.success(self.request, "You're bannd from this j")
                return redirect('home')
            return super(LinkCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'You are not allowed to post now, please try again later')
            return redirect("home")

class LinkDetailView(FormMixin, DetailView):
    models		= Link
    queryset 	= Link.objects.all()

    def get_success_url(self):
        return reverse('link_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})
    # form_class  = CommentForm
    # def get_context_data(self, **kwargs):
    #     context = super(LinkDetailView, self).get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     context['comments'] = self.object.comments.all()
    #     return context

    def get_context_data(self, **kwargs):
        context = super(LinkDetailView, self).get_context_data(**kwargs)
        context['moderate_by_current_user'] = Jaryanak.objects.filter(moderators__exact=self.request.user.id)
        context['reasons'] = REASON_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        link = get_object_or_404(Link, pk=self.object.pk)
        f = form.save(commit=False)
        f.user = self.request.user
        f.link = link
        f.save()
        return super(LinkDetailView, self).form_valid(form)

class LinkUpdateView(UpdateView):
    model       = Link
    form_class  = LinkForm

class LinkDeleteView(DeleteView):
    model       = Link
    success_url = reverse_lazy("home")

class TextCreateView(CreateView):
    model       = Text
    form_class  = TextForm
    template_name = "links/text_form.html"

    def form_valid(self, form):
        # REMOVE "NOT" IN PRODUCTION!!
        if allowed_to_post(self.request, self.request.user):
            f = form.save(commit=False)
            f.submitter = self.request.user
            f.ip = get_client_ip(self.request)
            if not f.submitter.userprofile.is_banned(f.jaryanak):
                f.save()
                get_favicon.delay(f.pk)
                messages.success(self.request, 'Your text has been sent')
            else:
                messages.success(self.request, "You're bannd from this j")
                return redirect('home')
            return super(TextCreateView, self).form_valid(form)
        else:
            return redirect("home")

            
class TextDetailView(FormMixin, DetailView):
    models      = Text
    queryset    = Text.objects.all()

    def get_success_url(self):
        return reverse('text_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})
    # form_class  = CommentForm
    # def get_context_data(self, **kwargs):
    #     context = super(LinkDetailView, self).get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     context['comments'] = self.object.comments.all()
    #     return context

    def get_context_data(self, **kwargs):
        context = super(TextDetailView, self).get_context_data(**kwargs)
        context['moderate_by_current_user'] = Jaryanak.objects.filter(moderators__exact=self.request.user.id)
        context['reasons'] = REASON_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        text = get_object_or_404(Text, pk=self.object.pk)
        f = form.save(commit=False)
        f.user = self.request.user
        f.text = text
        f.save()
        return super(TextDetailView, self).form_valid(form)

class TextUpdateView(UpdateView):
    model       = Text
    form_class  = TextForm

class TextDeleteView(DeleteView):
    model       = Text
    success_url = reverse_lazy('home')

class UserProfileDetailView(DetailView):
    model       = get_user_model()
    slug_field 	= "username"
    template_name = "profile/profile_detail.html"

    # def get_object(self, queryset=None):
    #     user 	= super(UserProfileDetailView, self).get_object(queryset)
    #     UserProfile.objects.get_or_create(user=user)
    #     return user

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        # context['up_voted_links'] = Link.objects.filter(votes__voter=self.object, votes__vote_type="0")
        # context['down_voted_links'] = Link.objects.filter(votes__voter=self.object, votes__vote_type="1")
        context['posts'] = Post.objects.filter(post__submitter__exact=self.object)
        context['comments'] = ThreadedComment.objects.filter(user__exact=self.object) 
        context['votes'] = Vote.objects.filter(user=self.object)
        context['votes_count'] = Vote.objects.filter(user=self.object).count()
        context['moderated'] = Jaryanak.objects.filter(moderators__exact=self.object)
        context['following'] = Jaryanak.objects.filter(followers__exact=self.object)
        context['is_admin'] = Jaryanak.objects.filter(admin__exact=self.object)
        # context['invitations'] = Invite.objects.filter(invitee__exact=self.object).filter(used__exact=False)
        return context

class UserProfileEditView(UpdateView):
    model 		= UserProfile
    form_class 	= UserProfileForm
    template_name = "profile/profile_edit.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})

class UserProfileInvitations(DetailView):
    model = get_user_model()
    slug_field  = "username"
    template_name = "profile/profile_invitations.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileInvitations, self).get_context_data(**kwargs)
        context['sent'] = Invite.objects.filter(inviter__exact=self.object)
        context['received'] = Invite.objects.filter(invitee__exact=self.object)
        context['invitations_list'] = sorted(chain(context['sent'], context['received']), key=lambda invite: invite.created_at, reverse=True)
        return context

class UserProfileReports(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = 'profile/profile_reports.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileReports, self).get_context_data(**kwargs)
        js = Jaryanak.objects.get_for_user(self.request.user)
        context['reports'] = []
        print js
        for j in js:
            r = Report.objects.get_report_for_jarayanak(j)
            context['reports'].append(r)
        return context

class JaryanakListView(ListView):
    model = Jaryanak 
    queryset    = Jaryanak.objects.all()
    paginate_by = 100

class JaryanakCreateView(CreateView):
    model       = Jaryanak
    form_class  = JaryanakForm
    template_name = "links/jaryanak_form.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.admin = self.request.user
        f.save()
        follow = Follow(user=self.request.user, jaryanak=f)
        follow.save()
        # jaryanak = Jaryanak.objects.get(pk=f.pk)
        # user = self.request.user 
        # mem = Membership(user=user, jaryanak=jaryanak)
        # mem.save()
        return super(JaryanakCreateView, self).form_valid(form)

class JaryanakUpdateView(UpdateView):
    model       = Jaryanak
    form_class  = JaryanakForm

class JaryanakDetailView(DetailView):
    models      = Jaryanak
    queryset    = Jaryanak.objects.all()

    def get_context_data(self, **kwargs):
        context = super(JaryanakDetailView, self).get_context_data(**kwargs)
        # context['links_categorized'] = Link.objects.filter(jaryanak__name=self.object)
        posts = Post.objects.all()
        posts_in_jaryanak = []
        for post in posts:
            if post.jaryanak == self.object:
                posts_in_jaryanak.append(post)
        context['posts_in_jaryanak'] = posts_in_jaryanak
        # context['posts_in_jaryanak'] = Post.objects.filter(post__jaryanak__name=self.object).order_by('-created_at')
        # context['category_count']    = Link.objects.filter(jaryanak__name=self.object).count()
        context['count'] = Post.objects.filter(post__jaryanak__name=self.object).count()

        # moderators
        jaryanak   = Jaryanak.objects.get(name=self.object)
        if self.request.user in jaryanak.followers.all():
            followed = True
        else:
            followed = False
        context['followed'] = followed
        context['moderators_list'] = jaryanak.moderators.all()
        context['followers'] =  jaryanak.followers.all()
        return context

    def get_success_url(self):
        return reverse('jaryanak_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Student').count() == 0, login_url='/myapp/denied/')
class JReportsView(ListView):
    template_name = 'flags/reports_on_j.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.jaryanak = get_object_or_404(Jaryanak, pk=pk)
        reports = Report.objects.get_report_for_jarayanak(self.jaryanak).order_by('-submit_date')
        return reports
        # qs=[]
        # for r in reports:
        #     if r.object.jaryanak == self.jaryanak:
        #         qs.append(r)

class AllReportsView(ListView):
    model = Report
    queryset = Report.objects.all().order_by('-submit_date')
    template_name = 'flags/reports_for_admin.html'
    paginate_by = 50 


def FollowView(request, pk, slug):
    jaryanak = get_object_or_404(Jaryanak, pk=pk)
    # followed = Follow.objects.get_for_user(user=request.user, jaryanak=jaryanak)
    if request.user in jaryanak.followers.all():
        followed = True
    else:
        followed = False
    # if request.method == 'Text':
    if 'next' in request.GET:
        next = request.GET['next']
    elif hasattr(jaryanak, 'get_absolute_url'):
        if callable(getattr(jaryanak, 'get_absolute_url')):
            next = jaryanak.get_absolute_url()
        else:
            next = jaryanak.get_absolute_url
    else:
        raise AttributeError('Define get_absolute_url')

    if followed:
        f = Follow.objects.get_for_user(user=request.user, jaryanak=jaryanak)
        f.delete()
    else:
        f = Follow(user=request.user, jaryanak=jaryanak)
        f.save()

    return HttpResponseRedirect(next)

def SearchJaryanaks(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    jaryanaks = Jaryanak.objects.filter(name__contains=search_text)
    most_viewed = Jaryanak.objects.all()
    return render_to_response('ajax_search.html', {'jaryanaks': jaryanaks})

#GET IP
    # http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if http_x_forwarded_for:
    #     ip_address = x_forwarded_for.split(',')[0]
    # else:
    #     ip_address = request.META.get('REMOTE_ADDR')
    # print ip_address



# class CommentCreateView(FormView):
#     form_class  = CommentForm
#     template_name = "comments/comment_form.html"

#     def form_valid(self, form):
#         link = get_object_or_404(Link, pk=form.data["link"])
#         print link
#         f = form.save(commit=False)
#         f.user = self.request.user
#         f.link = link
#         f.save()
#         return super(CommentCreateView, self).form_valid(form)

# class VoteFormView(FormView):
#     form_class = VoteForm

#     def form_valid(self, form):
#         v_user = self.request.user
#         v_link = get_object_or_404(Link, pk=form.data["link"])
#         v_type = form.data['vote_type']

#         voted       = Vote.objects.filter(voter=v_user, link=v_link)
#         up_voted    = Vote.objects.filter(voter=v_user, link=v_link, vote_type=0)
#         down_voted  = Vote.objects.filter(voter=v_user, link=v_link, vote_type=1)

#         if v_type == '1':
#             if down_voted:
#                 print "%s down vote removed from %s " % (v_user, v_link)
#                 down_voted[0].delete()
#                 Link.objects.vote_down(form.data["link"], increment=False)
#             elif not voted:
#                 print "%s down voted %s " % (v_user, v_link)
#                 Vote.objects.create(voter=v_user, link=v_link, vote_type=v_type)
#                 Link.objects.vote_down(form.data["link"])
#         else:
#             if up_voted:
#                 print "%s up vote removed from %s " % (v_user, v_link)
#                 up_voted[0].delete()
#                 Link.objects.vote_up(form.data["link"], increment=False)
#             elif not voted:
#                 print "%s up voted %s " % (v_user, v_link)
#                 Vote.objects.create(voter=v_user, link=v_link, vote_type=v_type)
#                 Link.objects.vote_up(form.data["link"])
#         return redirect("home")

#     def form_invalid(slef, form):
#         print("invalid")
#         return redirect("home")

# class TagsListView(ListView):
#     model       = Tag

# class TagsDetailView(DetailView):
#     models      = Tag
#     queryset    = Tag.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super(TagsDetailView, self).get_context_data(**kwargs)
#         context['links_tagged'] = Link.objects.filter(tags__name=self.object)
#         context['tag_count']    = Link.objects.filter(tags__name=self.object).count()
#         return context

# class CategoryDetailView(DetailView):
#     model   = Category
#     queryset = Category.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super(CategoryDetailView, self).get_context_data(**kwargs)
#         context['links_categorized'] = Link.objects.filter(category__name=self.object)
#         context['category_count']    = Link.objects.filter(category__name=self.object).count()
#         return context