# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0049_auto_20151120_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
