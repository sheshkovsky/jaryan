# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_auto_20151113_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
