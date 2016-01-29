from django.contrib import admin
from .models import Entry
from django_markdown.admin import MarkdownModelAdmin

# Register your models here.
class EntryAdmin(MarkdownModelAdmin):
	list_display = ('id', 'title', 'created', 'publish')
	prepopulated_fields = {'slug': ('title',), }

admin.site.register(Entry, EntryAdmin)