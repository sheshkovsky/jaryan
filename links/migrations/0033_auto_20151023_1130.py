# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0032_auto_20151020_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='link',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='voter',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
