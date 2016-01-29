# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import links.thumbs


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0050_auto_20151120_2213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-submit_date']},
        ),
        migrations.RenameField(
            model_name='link',
            old_name='ip',
            new_name='modifier_ip',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='update_date',
            new_name='modify_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='created_at',
            new_name='submit_date',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='ip',
            new_name='modifier_ip',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='update_date',
            new_name='modify_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='rank_score',
        ),
        migrations.AddField(
            model_name='jaryanak',
            name='logo',
            field=links.thumbs.ImageWithThumbsField(upload_to=b'images/logo_pictures/', blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='modified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='link',
            name='modifier',
            field=models.ForeignKey(related_name='link_modifier', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='submitter_ip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='modified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='text',
            name='modifier',
            field=models.ForeignKey(related_name='text_modifier', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='submitter_ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
