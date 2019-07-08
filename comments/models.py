import uuid

from django.db import models
from django.conf import settings

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import RandomCharField

from core.mixins import VoteMixin
from ideas.models import Idea

class Comment(VoteMixin, TimeStampedModel):
    content = models.CharField(max_length = 1055, blank = True, null = True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )

    idea = models.ForeignKey(
        Idea,
        on_delete = models.CASCADE,
        null = True,
        blank = True
    )
    comment = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'comments'
    )
    rand_id = RandomCharField(length=12, null = True)

    up_voted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comments_up_voted')
    down_voted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comments_down_voted')

    def get_comments(self):
        qs = Comment.objects.filter(comment = self)
        return qs
