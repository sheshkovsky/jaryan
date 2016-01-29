# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_auto_20151113_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='status',
            field=models.IntegerField(default=2, choices=[(0, b'Accepted'), (1, b'Rejected'), (2, b'Pending'), (3, b'Expired')]),
        ),
    ]
