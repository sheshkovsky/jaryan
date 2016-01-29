# -*- coding: utf-8 -*-

def slugify_persian(str):
	# self.slug = slugify(self.title)
	str = str.replace(u'،', "-")
	str = str.replace(u'، ', "-")
	str = str.replace("(", "-")
	str = str.replace(")", "")
	str = str.replace( u'؟', "")
	str = str.replace( u'?', "")
	str = str.replace( u'!', "")
	str = '-'.join(str.lower().split(' '))
	return "%s" % str