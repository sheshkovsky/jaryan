# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0046_auto_20151118_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='text',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='jaryanak',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AddField(
            model_name='thread',
            name='jaryans',
            field=models.ManyToManyField(related_name='jaryans', to='links.Jaryanak'),
        ),
    ]
