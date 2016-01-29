# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0035_auto_20151031_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joind', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='jaryanak',
            name='moderators',
            field=models.ManyToManyField(related_name='moderater', through='links.Membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='jaryanak',
            field=models.ForeignKey(to='links.Jaryanak'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='followers',
            field=models.ManyToManyField(related_name='follower', through='links.Follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
