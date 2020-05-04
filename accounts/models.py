from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import hashlib

# settings.AUTH_USER_MODEL  == string
# get_user_model() == class


class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

    @property
    def gravatar_url(self):
        return f"https://s.gravatar.com/avatar/{hashlib.md5(self.email.encode('utf-8').strip().lower()).hexdigest()}?s=170&d=mp"