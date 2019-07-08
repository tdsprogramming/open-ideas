from django.urls import path, include

from .views import (
    comment_up_vote_view,
    comment_down_vote_view,
    comment_create_view,
    comment_delete_view
)

app_name = 'comments'

urlpatterns = [
    path('up_vote/<int:id>/', comment_up_vote_view, name = 'up_vote'),
    path('down_vote/<int:id>/', comment_down_vote_view, name = 'down_vote'),
    path('create/<str:idea_slug>/<str:comment_id>/', comment_create_view, name = 'create'),
    path('delete/<int:id>/', comment_delete_view, name = 'delete')
]
