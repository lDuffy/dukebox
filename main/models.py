import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=True, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

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
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    username = models.CharField(_('username'),  max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    checked_in_event = models.ForeignKey('Event', default=None, blank=True, null=True)

    token = models.ForeignKey(Token, default=None, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)


class Song(BaseModel):
    title = models.CharField(_('title'), max_length=30, blank=True)
    event = models.ForeignKey(Event, default=None, related_name="songs")
    cmsUser = models.ForeignKey(CmsUser, default=None, related_name="posted_by")
    count = models.IntegerField(default=0)
    chosen = models.BooleanField(default=False)
