from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView

from .models import Comment
from ideas.models import Idea

def comment_up_vote_view(request, id):
    # get previous view
    comment = Comment.objects.get(id=id)
    comment.up_vote(request.user)
    context = {
        'votes': comment.net_votes
    }
    return JsonResponse(context)

def comment_down_vote_view(request, id):
    comment = Comment.objects.get(id=id)
    comment.down_vote(request.user)
    context = {
        'votes': comment.net_votes
    }
    return JsonResponse(context)

def comment_create_view(request, idea_slug, comment_id = None):
    idea = get_object_or_404(Idea, slug = idea_slug)
    comment = Comment.objects.create(
        idea = idea,
        content = request.POST['content'],
        author = request.user
    )
    # if comment_id:
    #     parent_comment = get_object_or_404(Comment, rand_id = comment_id)
    #     comment.comment = parent_comment
    #     comment.save()
    print('test', request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def comment_delete_view(request, id):
    Comment.objects.filter(id = id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
