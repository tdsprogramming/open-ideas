from django.urls import path

from .views import (
    idea_up_vote_view,
    idea_down_vote_view,
    claim_idea_view,
    IdeaCreateView,
    IdeaDetailView,
    IdeaListView,

)

app_name = 'ideas'

urlpatterns = [
    path('up_vote/<str:slug>/', idea_up_vote_view, name='up_vote'),
    path('down_vote/<str:slug>/', idea_down_vote_view, name='down_vote'),
    path('claim/<str:slug>/', claim_idea_view, name='claim'),
    path('', IdeaListView.as_view(), name='list'),
    path('new/', IdeaCreateView.as_view(), name='create'),
    path('<str:slug>/', IdeaDetailView.as_view(), name='detail'),

]
