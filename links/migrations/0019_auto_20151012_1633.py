# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0018_auto_20151012_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='domain',
            field=models.CharField(default='google.com', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=b'images/profile_pictures/', blank=True),
        ),
    ]
