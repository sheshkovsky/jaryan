# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0017_auto_20151012_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'images/profile_pictures/default.jpg', upload_to=b'images/profile_pictures/', width_field=150, height_field=150, blank=True),
        ),
    ]
