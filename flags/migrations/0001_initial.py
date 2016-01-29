# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0048_userprofile_ip'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='bookmarker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['submit_date'],
                'db_table': 'bookmarks',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.IntegerField(default=0, choices=[(0, b'Spam'), (1, b'Vote Manipulation'), (2, b'Personal Info'), (3, b'Abusive'), (4, b'Breaking Jaryan'), (5, b'Other')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Banned for 1 day'), (2, b'Banned for 3 days'), (3, b'Banned for 10 days'), (4, b'Banned forever'), (5, b'Post unpubished'), (6, b'No action needed')])),
                ('date_moderated', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('jaryanak', models.ForeignKey(related_name='jaryanak', to='links.Jaryanak')),
                ('moderater', models.ForeignKey(related_name='moderator', to=settings.AUTH_USER_MODEL, null=True)),
                ('reporter', models.ForeignKey(related_name='reporters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['submit_date'],
                'db_table': 'reports',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together=set([('user', 'content_type', 'object_id')]),
        ),
    ]
