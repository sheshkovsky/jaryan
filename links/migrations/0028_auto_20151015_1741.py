# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0027_link_rank_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='rank_score',
            field=models.FloatField(default=0.0),
        ),
    ]
