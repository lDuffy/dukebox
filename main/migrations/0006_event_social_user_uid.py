# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160907_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='social_user_uid',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
