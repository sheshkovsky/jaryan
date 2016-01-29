# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_link_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='slug',
        ),
    ]
