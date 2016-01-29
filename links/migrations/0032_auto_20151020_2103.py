# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0031_auto_20151020_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=models.CharField(max_length=200, db_index=True),
        ),
    ]
