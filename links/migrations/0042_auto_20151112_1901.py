# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import links.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0041_auto_20151110_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaryanak',
            name='invitations',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='logo',
            field=links.thumbs.ImageWithThumbsField(upload_to=b'images/jaryanak_logos/', blank=True),
        ),
    ]
