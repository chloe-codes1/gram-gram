from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# settings.AUTH_USER_MODEL  == string
# get_user_mdoe() == class


class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

