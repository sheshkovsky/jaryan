# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0011_remove_link_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 10, 8, 20, 0, 20, 382046, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
    ]
