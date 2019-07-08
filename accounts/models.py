import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.contrib.sessions.models import Session

class ClientUser(AbstractUser):
    github_profile = models.URLField()
    slug = AutoSlugField(populate_from = 'username')
    socket_update = models.BooleanField(default = True)
