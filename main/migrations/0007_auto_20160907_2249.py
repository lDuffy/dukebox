# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_event_social_user_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='social_user_uid',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
