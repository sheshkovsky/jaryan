# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0033_auto_20151023_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jaryanak',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=400, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('jaryanak', models.ForeignKey(to='links.Jaryanak')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SampleCount',
        ),
        migrations.RemoveField(
            model_name='link',
            name='category',
        ),
        migrations.RemoveField(
            model_name='link',
            name='down_votes',
        ),
        migrations.RemoveField(
            model_name='link',
            name='up_votes',
        ),
        migrations.AddField(
            model_name='link',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 31, 17, 59, 51, 455634, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='moderators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='links.Membership'),
        ),
        migrations.AddField(
            model_name='link',
            name='jaryanak',
            field=models.ForeignKey(default=1, to='links.Jaryanak'),
        ),
    ]
