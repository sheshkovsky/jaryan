# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0040_auto_20151101_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(null=True)),
                ('rank_score', models.FloatField(default=0.0)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200, db_index=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('rank_score', models.FloatField(default=0.0)),
                ('nsfw_flag', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='admin',
            field=models.ForeignKey(related_name='admin', default='0', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notify_me',
            field=models.IntegerField(default=0, choices=[(0, b'Instantly'), (1, b'Daily'), (2, b'Weekly'), (3, b'Never')]),
        ),
        migrations.AddField(
            model_name='text',
            name='jaryanak',
            field=models.ForeignKey(default=1, to='links.Jaryanak'),
        ),
        migrations.AddField(
            model_name='text',
            name='language',
            field=models.ForeignKey(default=1, to='links.Language'),
        ),
        migrations.AddField(
            model_name='text',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
