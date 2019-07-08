import json

from django.db import models
from django.conf import settings

import requests
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

from ideas.models import Idea

class Project(TimeStampedModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null = True, related_name = 'created_projects')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, null = True, related_name = 'collaborated_projects')
    repo_url = models.URLField(blank = True, null = True)
    idea = models.ForeignKey(Idea, on_delete = models.CASCADE, blank = True, null = True)
    name = models.CharField(max_length = 50, blank=True, null=True)
    slug = AutoSlugField(populate_from = ['idea', 'creator'], null = True)
    languages = models.CharField(max_length = 500, blank = True, null = True)

    def get_repo_information(self):
        github_repo_information = self.repo_url.split("github.com")[1].split('/')
        github_user = github_repo_information[1]
        github_repository_name = github_repo_information[2]
        request_url = 'https://api.github.com/repos/{}/{}'.format(github_user, github_repository_name)

        r = requests.get(request_url)
        content = json.loads(r.text)
        data = {
            'forks': content['forks_count'],
            'stars': content['stargazers_count'],
            'watchers': content['watchers_count'],
            'updated_at': content['updated_at'],
        }

        r = requests.get(request_url + '/languages')
        content = json.loads(r.text)

        total_lines = 0
        for k, v in content.items():
            total_lines += v

        for k,v in content.items():
            content[k] = str(round(v/total_lines * 100, 2))+"%"
        data['languages'] = content

        r = requests.get(request_url + '/collaborators')
        content = json.loads(r.text)
        data['collaborators'] = len(content)

        return data

    def __str__(self):
        return "{}".format(self.idea)
        # 1. Connect to Github's API and repository stats
        # 2. Get the list of languagues, put it in list and json dump it
        # 3. Get collaborators, forks, stars, etc.
        # 4. Get list of issues
