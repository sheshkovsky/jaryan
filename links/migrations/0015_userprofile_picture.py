# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0014_auto_20151011_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=datetime.datetime(2015, 10, 12, 9, 13, 2, 503075, tzinfo=utc), upload_to=b'/images/profile_pictures/'),
            preserve_default=False,
        ),
    ]
