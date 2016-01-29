# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0016_auto_20151012_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'/Users/ali/Developer/altio/altio/media/images/profile_pictures/default.jpg', upload_to=b'images/profile_pictures/', blank=True),
        ),
    ]
