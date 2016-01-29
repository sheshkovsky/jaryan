# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import links.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0025_auto_20151013_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=links.thumbs.ImageWithThumbsField(upload_to=b'images/profile_pictures/', blank=True),
        ),
    ]
