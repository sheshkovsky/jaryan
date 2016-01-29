# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0026_auto_20151015_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='rank_score',
            field=models.IntegerField(default=0),
        ),
    ]
