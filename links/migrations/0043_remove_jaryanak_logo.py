# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0042_auto_20151112_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jaryanak',
            name='logo',
        ),
    ]
