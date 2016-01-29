# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0003_invite_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 13, 22, 13, 5, 503131)),
        ),
    ]
