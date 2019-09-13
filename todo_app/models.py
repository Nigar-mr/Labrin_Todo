import random
import string
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    profile_image = models.ImageField(_('Profile image'), upload_to='', null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def get_image(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return "/static/img/avataaars.svg"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_username(self):
        return self.username

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



User = MyUser

def generate_token(size=120, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120, default=generate_token)

    expire = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.token}"

    def get_verify_url(self):
        return reverse("verify_passw", kwargs={"token": self.token,
                                               "user_id": self.user_id})

class Unique(models.Model):
    page_name = models.CharField(max_length=25)
    background = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    copyright = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.page_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    name = models.CharField(max_length=50, null=True, blank=True)
    more = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    shared_user = models.ManyToManyField(User, related_name='shared_list')


class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=255)

    publish_date = models.DateTimeField(auto_now_add=True)