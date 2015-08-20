import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.conf import settings
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
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Subscribe to user save events to create API token for new users
    http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """
    if created:
        Token.objects.create(user=instance)


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
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

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


class AppUser(BaseModel):
    user = models.OneToOneField(CmsUser, related_name='app_user', null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return self.user.email


class Event(BaseModel):
    title = models.CharField(_('title'), max_length=30, blank=True)
    appUser = models.ForeignKey(AppUser, default=None)


class Song(BaseModel):
    title = models.CharField(_('title'), max_length=30, blank=True)
    event = models.ForeignKey(Event, default=None, related_name="songs")
    appUser = models.ForeignKey(AppUser, default=None)
    count = models.IntegerField(default=0)
    chosen = models.BooleanField(default=False)
