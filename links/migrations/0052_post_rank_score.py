# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0051_auto_20151121_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rank_score',
            field=models.FloatField(default=0.0),
        ),
    ]
