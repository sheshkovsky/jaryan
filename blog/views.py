from django.shortcuts import render
from django.views import generic
from .models import Entry

class BlogIndex(generic.ListView):
	queryset = Entry.objects.published()
	paginate_by = 5

class BlogDetail(generic.DetailView):
	model = Entry
