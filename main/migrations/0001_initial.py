# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.utils.datetime_safe
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='username', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'db_table': 'cms_user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('title', models.CharField(max_length=30, verbose_name='title', blank=True)),
                ('long', models.FloatField(null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('details', models.CharField(max_length=300, null=True, blank=True)),
                ('place', models.CharField(max_length=300, null=True, blank=True)),
                ('start_date', models.DateField(default=django.utils.datetime_safe.datetime.now, blank=True)),
                ('end_date', models.DateField(default=django.utils.datetime_safe.datetime.now, blank=True)),
                ('creator', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('cmsUser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('title', models.CharField(max_length=30, verbose_name='title', blank=True)),
                ('chosen', models.BooleanField(default=False)),
                ('cmsUser', models.ForeignKey(related_name='posted_by', default=None, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(related_name='songs', default=None, to='main.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='like',
            name='song',
            field=models.ForeignKey(to='main.Song'),
        ),
        migrations.AddField(
            model_name='cmsuser',
            name='checked_in_event',
            field=models.ForeignKey(default=None, blank=True, to='main.Event', null=True),
        ),
        migrations.AddField(
            model_name='cmsuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='cmsuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('song', 'cmsUser')]),
        ),
    ]
