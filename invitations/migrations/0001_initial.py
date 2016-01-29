# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0042_auto_20151112_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitee', models.ForeignKey(related_name='invitee', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(related_name='inviter', to=settings.AUTH_USER_MODEL)),
                ('jaryanak', models.ForeignKey(to='links.Jaryanak')),
            ],
        ),
    ]
