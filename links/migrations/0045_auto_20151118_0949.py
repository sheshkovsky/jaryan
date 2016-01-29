# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0044_userprofile_banned_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='banned_from',
            field=models.ManyToManyField(related_name='banned_jaryan', to='links.Jaryanak', blank=True),
        ),
    ]
