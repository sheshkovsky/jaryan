# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
