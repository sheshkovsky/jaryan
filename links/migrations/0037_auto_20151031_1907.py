# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0036_auto_20151031_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaryanak',
            name='followers',
            field=models.ManyToManyField(related_name='followers', through='links.Follow', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jaryanak',
            name='moderators',
            field=models.ManyToManyField(related_name='moderaters', through='links.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
