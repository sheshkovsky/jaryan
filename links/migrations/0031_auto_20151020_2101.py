# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0030_auto_20151018_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=models.CharField(unique=True, max_length=200, db_index=True),
        ),
    ]
