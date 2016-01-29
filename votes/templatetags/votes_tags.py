from django import template
from django.contrib.contenttypes.models import ContentType

from votes.models import Vote

register = template.Library()

@register.tag
def vote_form(parser, token):
	bits = token.split_contents()
	return VoteFormNode(*bits[1:])

class VoteFormNode(template.Node):
	def __init__(self, obj, tpl=None):
		self.obj = template.Variable(obj)
		self.tpl = 'votes/vote_form.html'

	def render(self, context):
		obj = self.obj.resolve(context)
		content_type = ContentType.objects.get_for_model(obj)
		return template.loader.render_to_string(self.tpl, {
            'object': obj,
            'content_type': content_type,},
            context_instance=context)

class ScoreForObjectNode(template.Node):
    def __init__(self, object, context_var):
        self.object = object
        self.context_var = context_var

    def render(self, context):
        try:
            object = template.resolve_variable(self.object, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = Vote.objects.get_score(object)
        return ''

# def do_vote_for_object(parser, token):
# 	bits = token.contents.split()
# 	if len(bits) != 2:
# 		raise template.TemplateSyntaxError("'%s' tag takes exactly one argument" % bits[0])
# 	return VoteForObjectNode()
	
def do_score_for_object(parser, token):
    """
    Retrieves the total score for an object and the number of votes
    it's received and stores them in a context variable which has
    ``score`` and ``num_votes`` properties.

    Example usage::

        {% score_for_object widget as score %}

        {{ score.score }}point{{ score.score|pluralize }}
        after {{ score.num_votes }} vote{{ score.num_votes|pluralize }}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return ScoreForObjectNode(bits[1], bits[3])

register.tag('score_for_object', do_score_for_object)
# register.tag('vote_for_object', do_vote_for_object)


@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)