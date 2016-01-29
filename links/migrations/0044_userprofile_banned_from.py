# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0043_remove_jaryanak_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='banned_from',
            field=models.ManyToManyField(related_name='banned_jaryan', null=True, to='links.Jaryanak'),
        ),
    ]
