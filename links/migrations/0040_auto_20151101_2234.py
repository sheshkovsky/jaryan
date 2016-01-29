# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0039_auto_20151101_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='nsfw_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 22, 34, 6, 836749, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='karma',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='nsfw_flag',
            field=models.BooleanField(default=False),
        ),
    ]
