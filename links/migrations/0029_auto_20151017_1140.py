# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0028_auto_20151015_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='link',
            name='favicon',
            field=models.URLField(blank=True),
        ),
    ]
