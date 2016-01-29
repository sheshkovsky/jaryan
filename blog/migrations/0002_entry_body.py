# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='body',
            field=models.TextField(default=datetime.datetime(2015, 11, 1, 20, 10, 55, 565874, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
