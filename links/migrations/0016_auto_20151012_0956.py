# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0015_userprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='blog',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'images/profile_pictures/default.jpg', upload_to=b'images/profile_pictures/', blank=True),
        ),
    ]
