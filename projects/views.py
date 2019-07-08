import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Project

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(*args, **kwargs)
        # context['github_stats'] = self.get_object().get_repo_information()
        context['github_stats'] = {
            'forks': 0,
            'stars': 2,
            'watchers': 2,
            'updated_at': datetime.datetime.strptime('2019-05-10T23:39:18Z'[:-1], '%Y-%m-%dT%H:%M:%S'),
            'languages': {
                'JavaScript': '94.8%',
                'HTML': '5.2%'
            },
            'collaborators': 2
        }
        return context

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/create.html'
    fields = [
        'name',
        'github_url',
    ]

def project_update_view(request, slug):
    project = Project.objects.get(slug = slug)
    if request.POST['new_name']:
        project.name = request.POST['new_name']
    project.save()
    return JsonResponse(model_to_dict(project))

def add_collaborator_to_project_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.collaborators.add(request.user)
    return redirect('projects:detail', slug=slug)
