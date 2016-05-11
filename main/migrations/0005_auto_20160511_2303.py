# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_event_geo_cords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='public',
            new_name='is_public',
        ),
    ]
