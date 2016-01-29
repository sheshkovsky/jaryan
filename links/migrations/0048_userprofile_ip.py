# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0047_auto_20151119_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
    ]
