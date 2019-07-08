from django.db import models
from django.conf import settings
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField

from core.mixins import VoteMixin

class Idea(VoteMixin, TimeStampedModel):
    title = models.CharField(max_length = 150)
    description = RichTextField()
    slug = AutoSlugField(populate_from = 'title')
    originator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True)

    up_voted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'ideas_up_voted')
    down_voted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'ideas_down_voted')

    djsearch_fields = [
        'title',
        'description'
    ]
    djresult_output = {
        'fields': [
            'title',
            'description'
        ]
    }
    def __str__(self):
        return "{}".format(self.title)

    def get_comments(self):
        from comments.models import Comment
        qs = Comment.objects.filter(idea = self)
        return qs

    def get_absolute_url(self, *args, **kwargs):
        return reverse('ideas:detail', kwargs={'slug':self.slug})
