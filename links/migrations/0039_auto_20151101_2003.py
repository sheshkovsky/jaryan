# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0038_auto_20151101_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaryanak',
            name='moderators',
            field=models.ManyToManyField(related_name='moderateors', through='links.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
