# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0013_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='down_votes',
            field=models.PositiveIntegerField(default=0, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='up_votes',
            field=models.PositiveIntegerField(default=0, db_index=True, blank=True),
        ),
    ]
