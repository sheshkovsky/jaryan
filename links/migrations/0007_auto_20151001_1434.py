# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_vote'),
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
