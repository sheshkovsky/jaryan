# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0045_auto_20151118_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='karma',
            field=models.IntegerField(default=1),
        ),
    ]
