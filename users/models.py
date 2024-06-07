import uuid

from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from core.utils import get_upload_path

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_('phone'), max_length=13, unique=True, blank=True, null=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(_('image'), upload_to=get_upload_path, blank=True, null=True)
    sex = models.CharField(_('sex'), max_length=2, choices=Sex.choices, default='')
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=20, blank=True, null=True)
    bio = models.TextField(_('biography'), max_length=150, blank=True, null=True)
    address = models.CharField(_('address'), max_length=128, blank=True, null=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name=_('user'))
    created_at = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now=True)

    def __str__(self):
        return f'{self.user} Profile'

    @property
    def name(self):
        if self.nickname:
            name = self.nickname
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except (FileNotFoundError, ValueError, AttributeError):
            avatar = static('images/avatar.svg')
        return avatar
