from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .models import Idea
from comments.forms import CommentForm
from comments.models import Comment
from projects.models import Project

def idea_up_vote_view(request, slug):
    '''
    Upvotes the a particular Idea
    '''
    idea = Idea.objects.get(slug=slug)
    idea.up_vote(request.user)
    context = {
        'votes': idea.net_votes
    }
    return JsonResponse(context)


def idea_down_vote_view(request, slug):
    '''
    Upvotes the a particular Idea
    '''
    idea = Idea.objects.get(slug=slug)
    idea.down_vote(request.user)
    context = {
        'votes': idea.net_votes
    }
    return JsonResponse(context)
    # Redirect to previous url

def claim_idea_view(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    projects = Project.objects.filter(idea = idea)
    already_has_project = False

    for p in projects:
        if p.creator == request.user:
            already_has_project = True

    if already_has_project:
        return render(request, 'ideas/claim.html', {
                'already_has_project': True,
                'project': Project.objects.get(creator=request.user, idea=idea)
            }
        )

    context = {
        'projects': projects,
        'idea': idea
    }
    if request.method == "POST":
        p = Project.objects.create(
            idea = idea,
            creator = request.user,
            name = request.POST['name']
        )
        return redirect('projects:detail', slug=p.slug)
    return render(request, 'ideas/claim.html', context = context)

class IdeaCreateView(CreateView):
    model = Idea
    template_name = 'ideas/create.html'
    fields = [
        'title',
        'description'
    ]

    def form_valid(self, form):
        self.object = form.save()

        # Make current user the originator
        self.object.originator = self.request.user
        self.object.save()
        return super().form_valid(form)

class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'ideas/detail.html'
    context_object_name = 'idea'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaDetailView, self).get_context_data(*args, **kwargs)
        context['projects'] = Project.objects.filter(idea = self.get_object())
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(idea = self.get_object()).order_by('-created')
        return context

class IdeaListView(ListView):
    model = Idea
    template_name = 'ideas/list.html'
    context_object_name = 'ideas'
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            filter_dict = {
                'pop_asc': 'net_votes',
                'pop_desc': '-net_votes',
                'new_asc': 'created',
                'new_desc': '-created',
            }
            order = filter_dict[self.request.GET.get('filter_by')]
            return Idea.objects.all().order_by(order)
        return Idea.objects.all()

# class IdeaUpdateView(UpdateView)
