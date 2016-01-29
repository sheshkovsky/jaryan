# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0007_auto_20151001_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_type', models.IntegerField(db_index=True, choices=[(0, b'Upvote'), (1, b'DownVote')])),
                ('vote_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('link', models.ForeignKey(related_name='votes', to='links.Link')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
