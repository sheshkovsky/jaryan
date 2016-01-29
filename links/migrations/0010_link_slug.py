# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0009_auto_20151006_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 10, 8, 19, 57, 19, 659134, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
    ]
