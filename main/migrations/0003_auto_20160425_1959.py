# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160413_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='playback_status',
            field=models.CharField(default=b'queued', max_length=10, choices=[(b'playing', b'Playing'), (b'paused', b'Paused'), (b'played', b'Played'), (b'queued', b'Queued')]),
        ),
        migrations.AddField(
            model_name='song',
            name='provider',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='provider_id',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
