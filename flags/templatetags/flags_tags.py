from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.tag
def report_form(parser, token):
	bits = token.split_contents()
	return ReportFormNode(*bits[1:])

class ReportFormNode(template.Node):
	def __init__(self, obj, tpl=None):
		self.obj = template.Variable(obj)
		self.tpl = 'flags/report_form.html'

	def render(self, context):
		obj = self.obj.resolve(context)
		content_type = ContentType.objects.get_for_model(obj)
		return template.loader.render_to_string(self.tpl, {
            'object': obj,
            'content_type': content_type,},
            context_instance=context)

@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)