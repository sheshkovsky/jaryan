# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('user_name', models.CharField(max_length=50, verbose_name="user's name", blank=True)),
                ('user_email', models.EmailField(max_length=254, verbose_name="user's email address", blank=True)),
                ('user_url', models.URLField(verbose_name="user's URL", blank=True)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='date/time submitted')),
                ('ip_address', models.GenericIPAddressField(unpack_ipv4=True, null=True, verbose_name='IP address', blank=True)),
                ('is_public', models.BooleanField(default=True, help_text='Uncheck this box to make the comment effectively disappear from the site.', verbose_name='is public')),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name='is removed')),
            ],
            options={
                'ordering': ('submit_date',),
                'db_table': 'comments',
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'permissions': [('can_moderate', 'Can moderate comments')],
            },
        ),
        migrations.CreateModel(
            name='CommentFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag', models.CharField(max_length=30, verbose_name='flag', db_index=True)),
                ('flag_date', models.DateTimeField(default=None, verbose_name='date')),
            ],
            options={
                'db_table': 'comments_flags',
                'verbose_name': 'comment flag',
                'verbose_name_plural': 'comment flags',
            },
        ),
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='comments.Comment')),
                ('title', models.TextField(verbose_name='Title', blank=True)),
                ('tree_path', models.CharField(verbose_name='Tree path', max_length=500, editable=False)),
                ('last_child', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='comments.ThreadedComment', null=True)),
                ('parent', models.ForeignKey(related_name='children', default=None, blank=True, to='comments.ThreadedComment', null=True, verbose_name='Parent')),
            ],
            options={
                'ordering': ('tree_path',),
                'db_table': 'threadedcomments_comment',
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=('comments.comment',),
        ),
        migrations.AddField(
            model_name='commentflag',
            name='comment',
            field=models.ForeignKey(related_name='flags', verbose_name='comment', to='comments.Comment'),
        ),
        migrations.AddField(
            model_name='commentflag',
            name='user',
            field=models.ForeignKey(related_name='comment_flags', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(related_name='content_type_set_for_comment', verbose_name='content type', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='comment',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comment_comments', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='commentflag',
            unique_together=set([('user', 'comment', 'flag')]),
        ),
    ]
