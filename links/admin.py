from django.contrib import admin
from .models import Post, Link, Text, UserProfile, Language, Jaryanak, Membership, Follow, Thread

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 

class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'content_type', 'object_id', 'content_object', 'submit_date', 'rank_score')

class LinkAdmin(admin.ModelAdmin):
	fieldsets = ((None,{
		'fields': ('url', 'title', 'description', 'jaryanak', 'language', 'rank_score', 'submitter', 'ip', 'published', 'nsfw_flag')
		}),
	)
	list_display = ('id', 'title', 'domain', 'jaryanak', 'submitter', 'rank_score','submit_date', 'published', 'nsfw_flag')

class TextAdmin(admin.ModelAdmin):
	fieldsets = ((None,{
		'fields': ('title', 'description', 'jaryanak', 'language', 'rank_score', 'submitter', 'submitter_ip', 'published', 'nsfw_flag')
		}),
	)
	list_display = ('id', 'title', 'jaryanak', 'submitter', 'rank_score', 'submit_date', 'modify_date', 'modified',  'published', 'nsfw_flag')

class UserProfileInline(admin.StackedInline):
	model 			= UserProfile
	can_delete 		= False


class UserProfileAdmin(UserAdmin):
	inlines			= (UserProfileInline,)

class LanguageAdmin(admin.ModelAdmin):
	model = Language
	prepopulated_fields = {'slug': ('name',), }

class JaryanakAdmin(admin.ModelAdmin):
	model = Jaryanak 
	list_display = ('id', 'name', 'admin', 'created_at')
	filter_horizontal = ('moderators',)

class MembershipAdmin(admin.ModelAdmin):
	list_display = ('user', 'jaryanak', 'date_joined')
	ordering = ['date_joined']

class FollowAdmin(admin.ModelAdmin):
	list_display = ('user', 'jaryanak')

class ThreadAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	prepopulated_fields = {'slug': ('name',), }


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Jaryanak, JaryanakAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.unregister(get_user_model())
admin.site.register(Post, PostAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Link, LinkAdmin)

admin.site.register(get_user_model(), UserProfileAdmin)

# class VoteAdmin(admin.ModelAdmin):
# 	list_display 	= ('voter', 'link', 'vote_type', 'vote_date')
# 	ordering 		= ['-vote_date']
# 	search_fields 	= ('link__title', 'voter__usernamename')

# class CommentAdmin(admin.ModelAdmin):
# 	list_display 	= ('user', 'link', 'comment', 'submit_date')
# 	ordering 		= ['-submit_date']

# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Vote, VoteAdmin)