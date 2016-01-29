# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0048_userprofile_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
