from django.contrib import admin
from flags.models import Report

class ReportAdmin(admin.ModelAdmin):
	fieldsets = ((None,{
		'fields': ('reporter', 'content_type', 'object_id', 'reason', 'status', 'ip', 'moderater',)
		}),
	)
	list_display = ('id', 'reporter', 'object', 'jaryanak', 'reason', 'status', 'ip', 'moderater', 'submit_date')

admin.site.register(Report, ReportAdmin)

# Register your models here.
