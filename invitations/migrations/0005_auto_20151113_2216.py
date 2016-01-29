# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0004_auto_20151113_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
