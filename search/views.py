from django.shortcuts import render
from django.http import JsonResponse

from djsearch.utils import search_db

from ideas.models import Idea

def search_view(request):
    context = {
        'results': search_db(request.GET['q'], format='queryset', models=[Idea])
    }
    return render(request, 'search/results.html', context)
