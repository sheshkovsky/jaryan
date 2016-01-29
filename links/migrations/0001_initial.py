# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('url', models.URLField(verbose_name=b'URL')),
                ('description', models.TextField(max_length=500)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
