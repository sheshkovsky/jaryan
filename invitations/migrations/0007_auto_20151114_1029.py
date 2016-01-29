# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0006_invite_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Accepted'), (2, b'Rejected'), (3, b'Expired')]),
        ),
    ]
