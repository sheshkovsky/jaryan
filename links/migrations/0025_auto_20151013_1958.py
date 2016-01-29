# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0024_auto_20151013_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=models.SlugField(),
        ),
    ]
