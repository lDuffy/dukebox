# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


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
        migrations.AlterField(
            model_name='event',
            name='geo_cords',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
    ]
