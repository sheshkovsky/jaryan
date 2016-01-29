# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0037_auto_20151031_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='submit_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
