# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0020_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.ForeignKey(default=0, to='links.Category'),
        ),
    ]
