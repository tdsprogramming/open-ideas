from django.urls import path

from .views import (
    ProjectDetailView,
    ProjectCreateView,
    project_update_view,
    add_collaborator_to_project_view
)

app_name = 'projects'

urlpatterns = [
    path('<str:slug>/', ProjectDetailView.as_view(), name='detail'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('update/<str:slug>/', project_update_view, name='update'),
    path('addcollab/<str:slug>/', add_collaborator_to_project_view, name='add_collaborator'),
]
