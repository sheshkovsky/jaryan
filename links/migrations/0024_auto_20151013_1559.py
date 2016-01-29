# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0023_auto_20151013_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='favicon',
            field=models.URLField(default=datetime.datetime(2015, 10, 13, 15, 59, 20, 54828, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='language',
            field=models.ForeignKey(default=1, to='links.Language'),
        ),
    ]
