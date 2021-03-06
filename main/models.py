import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from rest_framework.authtoken.models import Token


class BaseModel(models.Model):
    order = models.PositiveIntegerField(default=1, blank=True, )
    publish = models.BooleanField(default=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.uid)


class CmsUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    username = models.CharField(_('username'), unique=True, max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    checked_in_event = models.ForeignKey('Event', default=None, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'cms_user'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.email


class Event(BaseModel):
    title = models.CharField(_('title'), max_length=30, blank=True)
    creator = models.ForeignKey(CmsUser, default=None)
    details = models.CharField(max_length=300, null=True, blank=True)
    place = models.CharField(max_length=300, null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    is_public = models.BooleanField(default=True)
    geo_cords = models.PointField(geography=True, null=True, blank=True)
    social_user_uid = models.CharField(max_length=300, null=True, blank=True)

    gis = models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title


class Song(BaseModel):
    PLAYING = 'playing'
    PAUSED = 'paused'
    PLAYED = 'played'
    QUEUED = 'queued'
    PLAYBACK_STATES = (
        (PLAYING, 'Playing'),
        (PAUSED, 'Paused'),
        (PLAYED, 'Played'),
        (QUEUED, 'Queued'),
    )

    title = models.CharField(_('title'), max_length=30, blank=True)
    event = models.ForeignKey(Event, default=None, related_name="songs")
    cmsUser = models.ForeignKey(CmsUser, default=None, related_name="posted_by")
    chosen = models.BooleanField(default=False)
    provider_id = models.CharField(max_length=300, null=True, blank=True)
    provider = models.CharField(max_length=30, null=True, blank=True)
    playback_status = models.CharField(max_length=10, choices=PLAYBACK_STATES, default=QUEUED)


class Like(BaseModel):
    song = models.ForeignKey(Song)
    cmsUser = models.ForeignKey(CmsUser)

    class Meta:
        unique_together = (('song', 'cmsUser'),)
